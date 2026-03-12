from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ===== SYSTEM SCHEMAS =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# ===== USER SCHEMAS =====
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    name: Optional[str] = None
    phone: Optional[str] = None
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ===== HIERARCHY SCHEMAS (MEANING -> WORD -> LESSON -> COURSE) =====

class MeaningBase(BaseModel):
    vietnamese: str
    example_en: Optional[str] = None
    example_vi: Optional[str] = None

class MeaningResponse(MeaningBase):
    id: str
    word_id: str
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True


class WordBase(BaseModel):
    english: str
    phonetic: Optional[str] = None
    part_of_speech: Optional[str] = None
    audio_url: Optional[str] = None
    cefr: Optional[str] = None

class WordResponse(WordBase):
    id: str
    lesson_id: str
    updated_at: datetime
    is_deleted: bool
    meanings: List[MeaningResponse] = []

    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    name: str
    sub_name: Optional[str] = None
    quantity_of_word: int = 0

class LessonResponse(LessonBase):
    id: str
    course_id: str
    updated_at: datetime
    is_deleted: bool
    words: List[WordResponse] = []

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    name: str
    description: str
    sub_description: Optional[str] = None

class CourseResponse(CourseBase):
    id: str
    updated_at: datetime
    is_deleted: bool
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True

# ===== SYNC SCHEMAS =====
class SyncRequest(BaseModel):
    last_sync_time: datetime

# Schema cho Push Request từ iOS (StudyRecord)
class StudyRecordCreate(BaseModel):
    id: str # UUID String tạo từ iOS
    word_id: str
    memory_level: int
    last_review: datetime
    next_review: datetime
    updated_at: datetime
    is_deleted: bool

class StudyRecordResponse(StudyRecordCreate):
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Các Record khác tương tự (LessonRecord... mình sẽ làm sau cho gọn)
