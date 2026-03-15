from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.sync.crud import crud_sync
from app.modules.sync.schema import StudyRecordCreate
from app.modules.sync.model import StudyRecord

class SyncService:
    @staticmethod
    def push_records(db: Session, user_id: str, records: list[StudyRecordCreate]) -> int:
        saved_count = 0
        for rp in records:
            server_record = crud_sync.get_study_record(db, rp.id)
            
            if server_record:
                if rp.updated_at > server_record.updated_at:
                    crud_sync.update_study_record(db, server_record, rp.model_dump())
                    saved_count += 1
            else:
                record_data = rp.model_dump()
                record_data["user_id"] = user_id
                crud_sync.create_study_record(db, record_data)
                saved_count += 1
        return saved_count

sync_service = SyncService()
