from pydantic import BaseModel, Field

from schemas.category_schema import Category


class ProductBase(BaseModel):
    name: str = Field(example="Product name")
    price: float = Field(example="14.80")
    stock: int = Field(example="5")
    enabled: bool = Field(default=None, example="1")


class ProductCreate(ProductBase):
    category_id: int = Field(example=1)


class ProductUpdate(ProductBase):
    category_id: int = Field(default=None, example=1)
    name: str = Field(default=None, example="Product update")
    price: float = Field(default=None, example="16.80")
    stock: int = Field(default=None, example="4")
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
