from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    error: str


ItemsType = TypeVar("ItemsType")


class BaseQueryResponseSchema(BaseModel, Generic[ItemsType]):
    count: int
    offset: int
    limit: int
    items: ItemsType
