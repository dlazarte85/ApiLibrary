from pydantic import BaseModel, Field, validator

from schemas.category_schema import Category


class ProductBase(BaseModel):
    name: str = Field(example="Product name")
    price: float = Field(example="14.80", gt=0)
    stock: int = Field(example="5", gt=0)
    enabled: bool = Field(default=None, example="1")

    @validator('name', each_item=True)
    def check_name_not_empty(cls, v):
        assert v != '', 'The name is required.'
        return v


class ProductCreate(ProductBase):
    category_id: int = Field(example=1)


class ProductUpdate(ProductBase):
    category_id: int = Field(default=None, example=1)
    name: str = Field(default=None, example="Product update")
    price: float = Field(default=None, example="16.80", gt=0)
    stock: int = Field(default=None, example="4", gt=0)
    deleted: bool = Field(default=None, example="1")


class Product(ProductBase):
    id: int
    deleted: bool
    category: Category | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Product Name",
                "price": 12.60,
                "stock": 8,
                "enabled": 1,
                "deleted": 0,
                "category": {}
            }
        }
