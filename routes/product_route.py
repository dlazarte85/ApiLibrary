from schemas import product_schema
from schemas.generic_response_schema import GenericResponse, GenericErrorResponse
from service import product_service, auth_service
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from utils import api_response

route = APIRouter(prefix="/api",
                  dependencies=[Depends(auth_service.get_current_user)],
                  responses={422: {"model": GenericErrorResponse}},
                  tags=["products"])


@route.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[list[product_schema.Product]],
    description="Show all products"
)
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    products = product_service.get_products(db, skip, limit)
    return api_response.success_response(products)


@route.get(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Show a product"
)
def get_product(id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.get_product_by_id(id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=GenericResponse[product_schema.Product],
    description="Create a new product"
)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    try:
        product = product_service.create_product(product, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.put(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Update a product"
)
def update_product(id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    try:
        product = product_service.update_product(product, id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.delete(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Delete a product"
)
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.delete_product(id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)
