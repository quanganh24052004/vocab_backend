from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import CurrentSession, CurrentUser, get_current_admin, CurrentAdmin
from app.core.response import response_base, ResponseModel
from app.modules.users.schema import GetUserDetail, UpdateUserParam
from app.modules.users.crud import crud_user

router = APIRouter()

@router.get("/me", summary="Lấy profile cá nhân")
def get_user_me(current_user: CurrentUser) -> ResponseModel[GetUserDetail]:
    return response_base.success(data=current_user)

@router.put("/me", summary="Cập nhật profile cá nhân")
def update_user_me(
    db: CurrentSession,
    current_user: CurrentUser,
    obj_in: UpdateUserParam
) -> ResponseModel[GetUserDetail]:
    user = crud_user.update(db, current_user, obj_in)
    return response_base.success(data=user, msg="Cập nhật thành công")

@router.get("/", summary="[Admin] Danh sách người dùng", dependencies=[Depends(get_current_admin)])
def get_users(db: CurrentSession, skip: int = 0, limit: int = 100) -> ResponseModel[List[GetUserDetail]]:
    users = crud_user.get_all(db, skip=skip, limit=limit)
    return response_base.success(data=users)

@router.delete("/{user_id}", summary="[Admin] Xóa người dùng", dependencies=[Depends(CurrentAdmin)])
def delete_user(db: CurrentSession, user_id: str) -> ResponseModel:
    success = crud_user.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return response_base.success(msg="Xóa thành công")
