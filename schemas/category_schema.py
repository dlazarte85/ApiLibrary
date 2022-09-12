from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(example="Category name")
    enabled: bool | None = Field(default=None, example="1")
    deleted: bool | None = Field(default=None, example="0")


class CategoryUpdate(CategoryBase):
    name: str | None = Field(default=None, example="Category Update")


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Category Name",
                "enabled": 1,
                "deleted": 0
            }
        }
