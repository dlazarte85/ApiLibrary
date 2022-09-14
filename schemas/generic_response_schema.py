from pydantic import BaseModel, Field
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class GenericResponse(GenericModel, Generic[DataT]):
    success: bool = Field(True)
    data: DataT | None = None


class GenericErrorResponse(BaseModel):
    success: bool = Field(False)
    error: dict = [{"loc": ["string", 0], "msg": "string", "type": "string"}]
