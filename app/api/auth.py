from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from .. import models, schemas
from ..database import get_db
from ..core import security

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    # 1. Kiểm tra xem email đã tồn tại hay chưa
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản với email này đã tồn tại trong hệ thống.",
        )
    
    # 2. Băm mật khẩu ra
    hashed_password = security.get_password_hash(user_in.password)
    
    # 3. Lưu vào Database
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends() # Form này nhận username (ở đây mình dùng email) và password từ request body
) -> Any:
    # 1. Tìm user qua email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Xác thực (Không có user, hoặc pass sai thì báo lỗi)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai email hoặc mật khẩu.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Nếu đúng, cấp phát JWT cho user 
    # Mình chỉ lưu user_id dạng String(8) vào nội dung "sub" của Token
    access_token = security.create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
