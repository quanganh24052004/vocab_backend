from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter()

# Dependency giả lập: Xác thực JWT token (sẽ update sau)
# async def get_current_user(token: str = Depends(oauth2_scheme)): ...

@router.post("/pull_courses", response_model=List[schemas.CourseResponse])
def pull_courses(
    request: schemas.SyncRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Kéo các Course (và Lesson, Word tĩnh) có thay đổi (updated_at > last_sync_time)
    """
    changed_courses = db.query(models.Course).filter(
        models.Course.updated_at >= request.last_sync_time
    ).all()
    return changed_courses

@router.post("/pull_study_records", response_model=List[schemas.StudyRecordResponse])
def pull_study_records(
    request: schemas.SyncRequest,
    # current_user: models.User = Depends(get_current_user), # Chưa mock user nên mình truyền user_id tạm
    db: Session = Depends(get_db)
) -> Any:
    """
    Kéo các tiến độ học từ vựng (StudyRecord) có thay đổi (updated_at > last_sync_time)
    """
    # Hardcode user_id tạm để test, sau này lấy từ `current_user.id` của JWT
    user_id = "test_usr" 
    
    changed_records = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == user_id,
        models.StudyRecord.updated_at >= request.last_sync_time
    ).all()
    return changed_records

@router.post("/push_study_records")
def push_study_records(
    records: List[schemas.StudyRecordCreate],
    db: Session = Depends(get_db)
) -> Any:
    """
    Nhận mảng StudyRecord (những thay đổi lúc offline) từ iOS
    So sánh `updated_at` lưu vào DB (Conflict Resolution đơn giản: Thằng nào mới hơn thì đè thằng kia)
    """
    user_id = "test_usr" # Giả lập Token lấy ra user_id
    
    saved_count = 0
    
    for rp in records:
        # Tìm xem record này có trên server chưa (quét trên App = UUID do App tạo)
        server_record = db.query(models.StudyRecord).filter(
            models.StudyRecord.id == rp.id
        ).first()
        
        if server_record:
            # Nếu iOS gửi bản cập nhật MỚI HƠN server => ghi đè
            if rp.updated_at > server_record.updated_at:
                server_record.memory_level = rp.memory_level
                server_record.last_review = rp.last_review
                server_record.next_review = rp.next_review
                server_record.updated_at = rp.updated_at
                server_record.is_deleted = rp.is_deleted
                saved_count += 1
        else:
            # Create mới Record
            new_record = models.StudyRecord(
                id=rp.id,
                user_id=user_id,
                word_id=rp.word_id,
                memory_level=rp.memory_level,
                last_review=rp.last_review,
                next_review=rp.next_review,
                updated_at=rp.updated_at,
                is_deleted=rp.is_deleted
            )
            db.add(new_record)
            saved_count += 1
            
    db.commit()
    
    return {
        "message": f"Sync thành công. Đã cập nhật/tạo mới {saved_count}/{len(records)} records.",
        "server_sync_time": datetime.utcnow() # Client sẽ save biến này làm mốc kéo data lần sau
    }
