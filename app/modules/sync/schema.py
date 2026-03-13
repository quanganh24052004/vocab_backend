from datetime import datetime
from pydantic import Field
from app.core.schema import SchemaBase

class SyncRequest(SchemaBase):
    last_sync_time: datetime = Field(description="Mốc thời gian đồng bộ cuối cùng")

class StudyRecordBase(SchemaBase):
    id: str = Field(description="UUID do app tạo hoặc ID server")
    word_id: str = Field(description="ID của từ")
    memory_level: int = Field(0, description="Mức độ ghi nhớ")
    last_review: datetime
    next_review: datetime
    updated_at: datetime
    is_deleted: bool = False

class StudyRecordCreate(StudyRecordBase):
    pass

class StudyRecordResponse(StudyRecordBase):
    user_id: str
    created_at: datetime
