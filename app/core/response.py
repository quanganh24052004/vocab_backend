from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")

class SchemaBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        from_attributes=True
    )

class ResponseModel(SchemaBase, Generic[T]):
    code: int = 200
    msg: str = "Request successful"
    data: T | None = None

class ResponseBase:
    @staticmethod
    def success(data: T | None = None, msg: str = "Request successful") -> ResponseModel[T]:
        return ResponseModel[T](code=200, msg=msg, data=data)

    @staticmethod
    def fail(code: int = 400, msg: str = "Request error", data: T | None = None) -> ResponseModel[T]:
        return ResponseModel[T](code=code, msg=msg, data=data)

response_base = ResponseBase()
