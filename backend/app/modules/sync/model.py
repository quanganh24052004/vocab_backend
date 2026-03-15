from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import string
import random

def generate_youtube_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class StudyRecord(Base):
    __tablename__ = "study_records"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    user_id = Column(String(8), ForeignKey("users.id"), index=True)
    word_id = Column(String(8), ForeignKey("words.id"), index=True)
    
    memory_level = Column(Integer, default=0)
    last_review = Column(DateTime(timezone=True))
    next_review = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="study_records")
    word = relationship("Word", back_populates="study_records")

class LessonRecord(Base):
    __tablename__ = "lesson_records"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    user_id = Column(String(8), ForeignKey("users.id"), index=True)
    lesson_id = Column(String(8), ForeignKey("lessons.id"), index=True)
    
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True))
    is_learn = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="lesson_records")
    lesson = relationship("Lesson")
