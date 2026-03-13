from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import string
import random

def generate_youtube_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(8), primary_key=True, index=True, default=generate_youtube_id)
    name = Column(String, index=True)
    description = Column(String)
    sub_description = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
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
    cefr = Column(String, nullable=True)
    
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
