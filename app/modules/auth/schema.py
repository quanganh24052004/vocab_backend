from pydantic import Field, EmailStr
from app.core.schema import SchemaBase

class AuthParam(SchemaBase):
    username: str = Field(description="Email của người dùng")
    password: str = Field(description="Mật khẩu")

class RegisterParam(SchemaBase):
    email: EmailStr = Field(description="Email đăng ký")
    password: str = Field(description="Mật khẩu")
    name: str | None = Field(None, description="Họ tên")

class Token(SchemaBase):
    access_token: str
    token_type: str = "bearer"

class TokenData(SchemaBase):
    id: str | None = None
