from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.core import security
from app.core.response import response_base, ResponseModel
from app.modules.auth.schema import RegisterParam, AuthParam, Token
from app.modules.users.schema import GetUserDetail
from app.modules.auth.service import auth_service

router = APIRouter()

@router.post("/register", summary="Đăng ký tài khoản mới")
def register(
    db: Annotated[Session, Depends(get_db)],
    obj_in: RegisterParam
) -> ResponseModel[GetUserDetail]:
    user = auth_service.register(db, obj_in)
    return response_base.success(data=user, msg="Đăng ký thành công")

@router.post("/login", summary="Đăng nhập lấy access token")
def login(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> ResponseModel[Token]:
    # OAuth2PasswordRequestForm expects username/password
    auth_param = AuthParam(username=form_data.username, password=form_data.password)
    user = auth_service.authenticate(db, auth_param)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.id})
    return response_base.success(data=Token(access_token=access_token))
