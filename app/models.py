from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

import string
import random

def generate_youtube_id(length=8):
    """Tạo chuỗi ngẫu nhiên 8 ký tự an toàn dùng làm ID"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ==========================================
# 1. CORE AUTH & USER SYSTEM
# ==========================================
class User(Base):
    __tablename__ = "users"
    # Sửa thành String 8 ký tự
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # User Profile (tương ứng với model User & Account bên iOS)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Quan hệ 1-Nhiều với History
    study_records = relationship("StudyRecord", back_populates="user", cascade="all, delete-orphan")
    lesson_records = relationship("LessonRecord", back_populates="user", cascade="all, delete-orphan")

# ==========================================
# 2. STATIC CONTENT HIERARCHY (Khóa học tĩnh)
# Course -> Lesson -> Word -> Meaning
# ==========================================
class Course(Base):
    __tablename__ = "courses"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    name = Column(String, index=True)
    description = Column(String)
    sub_description = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 2 Cột phục vụ Delta Sync (Pull)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    course_id = Column(String(8), ForeignKey("courses.id"), index=True)
    
    name = Column(String, index=True)
    sub_name = Column(String, nullable=True)
    quantity_of_word = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    course = relationship("Course", back_populates="lessons")
    words = relationship("Word", back_populates="lesson", cascade="all, delete-orphan")

class Word(Base):
    __tablename__ = "words"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    lesson_id = Column(String(8), ForeignKey("lessons.id"), index=True)
    
    english = Column(String, index=True)
    phonetic = Column(String, nullable=True)
    part_of_speech = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    cefr = Column(String, nullable=True) # Level: A1, B2...
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    lesson = relationship("Lesson", back_populates="words")
    meanings = relationship("Meaning", back_populates="word", cascade="all, delete-orphan")
    study_records = relationship("StudyRecord", back_populates="word", cascade="all, delete-orphan")

class Meaning(Base):
    __tablename__ = "meanings"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    word_id = Column(String(8), ForeignKey("words.id"), index=True)
    
    vietnamese = Column(String)
    example_en = Column(String, nullable=True)
    example_vi = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    word = relationship("Word", back_populates="meanings")

# ==========================================
# 3. DYNAMIC CONTENT (Cá nhân hóa & Delta Sync Push)
# StudyRecord, LessonRecord
# ==========================================
class StudyRecord(Base):
    __tablename__ = "study_records"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    user_id = Column(String(8), ForeignKey("users.id"), index=True)
    word_id = Column(String(8), ForeignKey("words.id"), index=True)
    
    memory_level = Column(Integer, default=0)
    last_review = Column(DateTime(timezone=True))
    next_review = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Delta Sync
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
    # Delta Sync
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="lesson_records")
    lesson = relationship("Lesson")