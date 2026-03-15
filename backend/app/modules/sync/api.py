from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from app.core.deps import CurrentSession, CurrentUser
from app.core.response import response_base, ResponseModel
from app.modules.sync.schema import SyncRequest, StudyRecordCreate, StudyRecordResponse
from app.modules.sync.crud import crud_sync
from app.modules.sync.service import sync_service

router = APIRouter()

@router.post("/pull_study_records", summary="Kéo tiến độ học từ vựng mới")
def pull_study_records(
    db: CurrentSession,
    current_user: CurrentUser,
    request: SyncRequest
) -> ResponseModel[List[StudyRecordResponse]]:
    records = crud_sync.get_study_records_after(db, current_user.id, request.last_sync_time)
    return response_base.success(data=records)

@router.post("/push_study_records", summary="Đẩy tiến độ học từ vựng lên server")
def push_study_records(
    db: CurrentSession,
    current_user: CurrentUser,
    records: List[StudyRecordCreate]
) -> ResponseModel[dict]:
    count = sync_service.push_records(db, current_user.id, records)
    return response_base.success(
        data={"updated_count": count},
        msg=f"Sync thành công. Đã cập nhật {count}/{len(records)} records."
    )
