from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    videos: List["Video"] = Relationship(back_populates="user")
    analyses: List["Analysis"] = Relationship(back_populates="user")

class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    file_path: str
    original_filename: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending") # pending, processing, completed, error
    
    user: Optional[User] = Relationship(back_populates="videos")
    analysis: Optional["Analysis"] = Relationship(back_populates="video")

class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: Optional[int] = Field(default=None, foreign_key="video.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    content_type: str = Field(index=True) # travel, shopping, recipe, etc.
    structured_data: str # Will store JSON string of the structured result
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    video: Optional[Video] = Relationship(back_populates="analysis")
    user: Optional[User] = Relationship(back_populates="analyses")
    conversations: List["Conversation"] = Relationship(back_populates="analysis")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: Optional[int] = Field(default=None, foreign_key="analysis.id")
    role: str # user, system
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    analysis: Optional[Analysis] = Relationship(back_populates="conversations")
