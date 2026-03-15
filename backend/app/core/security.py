from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.conf import settings

ALGORITHM = settings.ALGORITHM

# Cấu hình Passlib để băm mật khẩu bằng thuật toán bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh mật khẩu gốc với mật khẩu đã băm trong database"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Băm mật khẩu ra chuỗi hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT Token để trả về cho iOS client khi Login thành công"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Cài cắm thời gian hết hạn (exp) vào token
    to_encode.update({"exp": expire})
    
    # Ký JWT bằng Secret Key và Algorithm
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
