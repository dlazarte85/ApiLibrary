from pydantic import BaseModel, Field, validator


class CategoryBase(BaseModel):
    name: str = Field(example="Category name")
    enabled: bool | None = Field(default=None, example="1")
    deleted: bool | None = Field(default=None, example="0")

    @validator('name', each_item=True)
    def check_name_not_empty(cls, v):
        assert v != '', 'The name is required.'
        return v


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
