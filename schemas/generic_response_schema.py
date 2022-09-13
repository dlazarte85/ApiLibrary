from pydantic import Field
from typing import Generic, TypeVar
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class GenericResponse(GenericModel, Generic[DataT]):
    success: bool = Field(True)
    data: DataT | None = None
