from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Sarthak API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sarthak API is running. Turn what you watch into something useful."}

import os
import shutil
from uuid import uuid4
from fastapi import BackgroundTasks, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from database import get_session
from models import Video
from worker import sync_process_video

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/v1/analyze")
async def analyze_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    mode: str = Form(default="general"),
    session: AsyncSession = Depends(get_session)
):
    """
    Receives media file, saves it locally, creates DB record, and queues it for AI processing.
    """
    if not file.content_type.startswith("video/") and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only video and image files are supported.")
    
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Create Database record
    db_video = Video(
        file_path=file_path,
        original_filename=file.filename,
        status="pending"
    )
    session.add(db_video)
    await session.commit()
    await session.refresh(db_video)
    
    # Queue background processing
    background_tasks.add_task(sync_process_video, db_video.id, file_path)
    
    return {
        "status": "success",
        "message": f"Media uploaded and queued for processing.",
        "video_id": db_video.id
    }

from schemas import TravelPlanRequest

@app.post("/api/v1/plan_travel")
async def plan_travel(
    request: TravelPlanRequest,
    session: AsyncSession = Depends(get_session)
):
    from models import Video, Analysis
    from ai_provider import GeminiProvider
    import json
    
    # 1. Ask Gemini to generate the plan
    provider = GeminiProvider()
    plan_dict = provider.generate_travel_plan(request.model_dump())
    
    # 2. Save a dummy Video and Analysis to DB so it shows in history
    db_video = Video(
        file_path="text_prompt",
        original_filename=f"Trip to {request.destination}",
        status="completed"
    )
    session.add(db_video)
    await session.commit()
    await session.refresh(db_video)
    
    db_analysis = Analysis(
        video_id=db_video.id,
        content_type="travel",
        structured_data=json.dumps(plan_dict)
    )
    session.add(db_analysis)
    await session.commit()
    await session.refresh(db_analysis)
    
    return {
        "status": "success",
        "video_id": db_video.id,
        "plan": plan_dict
    }

@app.post("/api/v1/shopping_chat")
async def shopping_chat(
    message: str = Form(""),
    session_id: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    from ai_provider import GeminiProvider
    
    image_path = None
    if file:
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"shop_{uuid4().hex}{file_extension}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
    provider = GeminiProvider()
    response_text = provider.shopping_chat(message=message, image_path=image_path)
    
    return {
        "status": "success",
        "response": response_text
    }

@app.post("/api/v1/recipe_chat")
async def recipe_chat(
    message: str = Form(""),
    session_id: str = Form(...)
):
    from ai_provider import GeminiProvider
    provider = GeminiProvider()
    response_text = provider.recipe_chat(message=message)
    
    return {
        "status": "success",
        "response": response_text
    }

from pydantic import BaseModel

class ChatRequest(BaseModel):
    analysis_id: int
    message: str

@app.post("/api/v1/chat")
async def chat_with_sarthak(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Allows the user to have a conversational interaction with the processed video content.
    """
    from models import Analysis, Conversation
    from sqlmodel import select
    from ai_provider import GeminiProvider
    
    # Fetch Analysis
    analysis = await session.get(Analysis, request.analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    # Fetch previous conversations
    statement = select(Conversation).where(Conversation.analysis_id == request.analysis_id).order_by(Conversation.created_at)
    results = await session.execute(statement)
    past_conversations = results.scalars().all()
    
    # Store user message
    user_msg = Conversation(analysis_id=request.analysis_id, role="user", message=request.message)
    session.add(user_msg)
    
    # Format history for AI
    history = [{"role": msg.role, "content": msg.message} for msg in past_conversations]
    
    # Get AI response
    provider = GeminiProvider()
    ai_response_text = provider.chat(
        user_message=request.message,
        context_data=analysis.structured_data,
        previous_messages=history
    )
    
    # Store system response
    sys_msg = Conversation(analysis_id=request.analysis_id, role="system", message=ai_response_text)
    session.add(sys_msg)
    await session.commit()
    
    return {
        "status": "success",
        "response": ai_response_text
    }

@app.get("/api/v1/videos/{video_id}/status")
async def get_video_status(video_id: int, session: AsyncSession = Depends(get_session)):
    from models import Video
    video = await session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"video_id": video.id, "status": video.status}

@app.get("/api/v1/analyses/{video_id}")
async def get_analysis(video_id: int, session: AsyncSession = Depends(get_session)):
    from models import Analysis
    from sqlmodel import select
    import json
    
    statement = select(Analysis).where(Analysis.video_id == video_id)
    results = await session.execute(statement)
    analysis = results.scalars().first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found or still processing")
        
    return {
        "analysis_id": analysis.id,
        "content_type": analysis.content_type,
        "data": json.loads(analysis.structured_data)
    }

@app.get("/api/v1/history")
async def get_history(session: AsyncSession = Depends(get_session)):
    from models import Analysis
    from sqlmodel import select
    import json
    
    statement = select(Analysis).order_by(Analysis.created_at.desc()).limit(20)
    results = await session.execute(statement)
    analyses = results.scalars().all()
    
    history = []
    for a in analyses:
        data = json.loads(a.structured_data)
        history.append({
            "analysis_id": a.id,
            "video_id": a.video_id,
            "content_type": a.content_type,
            "title": data.get("title", "Unknown"),
            "created_at": a.created_at
        })
        
    return {"history": history}
