from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import string
import random

def generate_youtube_id(length=8):
    """Tạo chuỗi ngẫu nhiên 8 ký tự an toàn dùng làm ID"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class User(Base):
    __tablename__ = "users"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # User Profile
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    role = Column(String, default="user") # "user" | "admin"
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Quan hệ
    study_records = relationship("StudyRecord", back_populates="user", cascade="all, delete-orphan", primaryjoin="User.id == StudyRecord.user_id")
    lesson_records = relationship("LessonRecord", back_populates="user", cascade="all, delete-orphan", primaryjoin="User.id == LessonRecord.user_id")
