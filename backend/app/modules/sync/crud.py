from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.sync.model import StudyRecord, LessonRecord

class CRUDSync:
    @staticmethod
    def get_study_records_after(db: Session, user_id: str, last_sync: datetime) -> list[StudyRecord]:
        return db.query(StudyRecord).filter(
            StudyRecord.user_id == user_id,
            StudyRecord.updated_at >= last_sync
        ).all()

    @staticmethod
    def get_study_record(db: Session, record_id: str) -> StudyRecord | None:
        return db.query(StudyRecord).filter(StudyRecord.id == record_id).first()

    @staticmethod
    def create_study_record(db: Session, obj_in: dict) -> StudyRecord:
        db_obj = StudyRecord(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_study_record(db: Session, db_obj: StudyRecord, update_data: dict) -> StudyRecord:
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_sync = CRUDSync()
