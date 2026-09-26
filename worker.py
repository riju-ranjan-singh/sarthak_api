import asyncio
import os
import json
from database import engine
from models import Video, Analysis
from sqlmodel import Session
from sqlalchemy.orm import sessionmaker

def sync_process_video(video_id: int, file_path: str):
    """
    Synchronous worker function that simulates a long-running AI extraction pipeline.
    In the future, this is where FFmpeg extraction, Gemini calls, and agent routing will happen.
    """
    print(f"[Worker] Started processing video {video_id} at {file_path}")
    
    # Setup synchronous session for background worker
    from sqlmodel import Session, create_engine
    # create sync engine for the worker (using the same sqlite path)
    sync_engine = create_engine(str(engine.url).replace("sqlite+aiosqlite", "sqlite"))
    
    with Session(sync_engine) as session:
        video = session.get(Video, video_id)
        if not video:
            print(f"[Worker] Video {video_id} not found!")
            return
            
        video.status = "processing"
        session.commit()
        
        # --- Video Processing Pipeline ---
        import os
        from video_processor import extract_audio, extract_keyframes
        
        video_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Audio Extraction
        audio_path = os.path.join(video_dir, f"{base_name}.mp3")
        extract_audio(file_path, audio_path)
        
        # Frame Extraction (1 frame per second)
        frames_dir = os.path.join(video_dir, f"{base_name}_frames")
        frames = extract_keyframes(file_path, frames_dir, fps=1)
        
        print(f"[Worker] Extracted {len(frames)} frames to {frames_dir}")
        
        # Use IntentRouter to detect the content type and get the correct Agent
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), "agents"))
        from intent_router import IntentRouter
        
        router = IntentRouter()
        agent = router.determine_intent(audio_path, frames)
        
        # The core video pipeline doesn't care which agent is returned!
        analysis_result = agent.process_media(audio_path=audio_path, frames=frames)
        
        # Pass the analysis through the Web Verification Engine
        from research_engine import VerificationEngine
        verifier = VerificationEngine()
        analysis_result = verifier.verify_analysis(intent=agent.intent_name, analysis_data=analysis_result)
        
        analysis = Analysis(
            video_id=video_id,
            content_type=analysis_result.get("content_type", "general"),
            structured_data=json.dumps(analysis_result)
        )
        session.add(analysis)
        
        video.status = "completed"
        session.commit()
        
    # --- Cleanup Temporary Media ---
    import shutil
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
        print(f"[Worker] Cleaned up temporary files for video {video_id}")
    except Exception as e:
        print(f"[Worker] Cleanup failed for video {video_id}: {e}")
        
    print(f"[Worker] Finished processing video {video_id}")
