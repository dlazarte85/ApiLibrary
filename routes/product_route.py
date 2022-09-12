from schemas import product_schema
from service import product_service, auth_service
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from utils import api_response

route = APIRouter(prefix="/api",
                  dependencies=[Depends(auth_service.get_current_user)],
                  tags=["products"])


@route.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=list[product_schema.Product],
    description="Show all products"
)
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return product_service.get_products(db, skip, limit)


@route.get(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=product_schema.Product,
    description="Show a product"
)
def get_product(id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(id, db)


@route.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=product_schema.Product,
    description="Create a new product"
)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(product, db)


@route.put(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=product_schema.Product,
    description="Update a product"
)
def update_product(id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_product(product, id, db)


@route.delete(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=product_schema.Product,
    description="Delete a product"
)
def delete_product(id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(id, db)
