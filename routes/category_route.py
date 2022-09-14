from schemas import category_schema
from schemas.generic_response_schema import GenericResponse, GenericErrorResponse
from service import category_service, auth_service
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from utils import api_response

route = APIRouter(prefix="/api",
                  dependencies=[Depends(auth_service.get_current_user)],
                  responses={422: {"model": GenericErrorResponse}},
                  tags=["categories"])


@route.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[list[category_schema.Category]],
    description="Show all categories"
)
def get_categories(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 20,
):
    categories = category_service.get_categories(db, skip=skip, limit=limit)
    return api_response.success_response(categories)


@route.get(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[category_schema.Category],
    description="Show a category"
)
def get_category(id: int, db: Session = Depends(get_db)):
    try:
        category = category_service.get_category_by_id(id, db)
        return api_response.success_response(category)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=GenericResponse[category_schema.Category],
    description="Create a new category"
)
def create_category(category: category_schema.CategoryBase, db: Session = Depends(get_db)):
    try:
        category = category_service.create_category(category, db)
        return api_response.success_response(category)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.put(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[category_schema.Category],
    description="Update a category"
)
def update_category(id: int, category: category_schema.CategoryUpdate, db: Session = Depends(get_db)):
    try:
        category = category_service.update_category(category, id, db)
        return api_response.success_response(category)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.delete(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[category_schema.Category],
    description="Delete a category"
)
def delete_category(id: int, db: Session = Depends(get_db)):
    try:
        category = category_service.delete_category(id, db)
        return api_response.success_response(category)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)
