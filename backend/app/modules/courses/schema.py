from datetime import datetime
from pydantic import Field
from app.core.schema import SchemaBase

# Meaning
class MeaningBase(SchemaBase):
    vietnamese: str = Field(description="Nghĩa tiếng Việt")
    example_en: str | None = Field(None, description="Ví dụ tiếng Anh")
    example_vi: str | None = Field(None, description="Ví dụ tiếng Việt")

class CreateMeaningParam(MeaningBase):
    pass

class GetMeaningDetail(MeaningBase):
    id: str
    word_id: str
    updated_at: datetime

# Word
class WordBase(SchemaBase):
    english: str = Field(description="Từ tiếng Anh")
    phonetic: str | None = Field(None, description="Phiên âm")
    part_of_speech: str | None = Field(None, description="Từ loại")
    audio_url: str | None = Field(None, description="Link audio")
    cefr: str | None = Field(None, description="Cấp độ CEFR")

class CreateWordParam(WordBase):
    pass

class GetWordDetail(WordBase):
    id: str
    lesson_id: str
    meanings: list[GetMeaningDetail] = []
    updated_at: datetime

# Lesson
class LessonBase(SchemaBase):
    name: str = Field(description="Tên bài học")
    sub_name: str | None = Field(None, description="Tên phụ bài học")
    quantity_of_word: int = Field(0, description="Số lượng từ")

class CreateLessonParam(LessonBase):
    pass

class GetLessonDetail(LessonBase):
    id: str
    course_id: str
    words: list[GetWordDetail] = []
    updated_at: datetime

# Course
class CourseBase(SchemaBase):
    name: str = Field(description="Tên khóa học")
    description: str = Field(description="Mô tả khóa học")
    sub_description: str | None = Field(None, description="Mô tả phụ")

class CreateCourseParam(CourseBase):
    pass

class BulkImportWordParam(CreateWordParam):
    meanings: list[CreateMeaningParam]

class BulkImportLessonParam(CreateLessonParam):
    words: list[BulkImportWordParam]

class BulkImportCourseParam(CreateCourseParam):
    lessons: list[BulkImportLessonParam]

class UpdateCourseParam(SchemaBase):
    name: str | None = None
    description: str | None = None
    sub_description: str | None = None
    is_deleted: bool | None = None

class GetCourseDetail(CourseBase):
    id: str
    lessons: list[GetLessonDetail] = []
    updated_at: datetime
    is_deleted: bool
