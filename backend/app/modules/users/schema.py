from datetime import datetime
from pydantic import Field
from app.core.schema import SchemaBase

class UserSchemaBase(SchemaBase):
    email: str | None = Field(None, description="Email")
    name: str | None = Field(None, description="Họ tên")
    phone: str | None = Field(None, description="Số điện thoại")
    role: str | None = Field(None, description="Vai trò (user/admin)")
    is_premium: bool = Field(False, description="Trạng thái Premium")

class GetUserDetail(UserSchemaBase):
    id: str
    created_at: datetime

class UpdateUserParam(SchemaBase):
    name: str | None = Field(None, description="Họ tên")
    phone: str | None = Field(None, description="Số điện thoại")
    is_premium: bool | None = Field(None, description="Trạng thái Premium")
