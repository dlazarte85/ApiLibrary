from schemas import category_schema
from service import category_service, auth_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.db import get_db

route = APIRouter(prefix="/api",
                  dependencies=[Depends(auth_service.get_current_user)],
                  tags=["categories"])


@route.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=list[category_schema.Category],
    description="Show all categories"
)
def get_categories(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 20,
):
    return category_service.get_categories(db, skip=skip, limit=limit)


@route.get(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=category_schema.Category,
    description="Show a category"
)
def get_category(id: int, db: Session = Depends(get_db)):
    return category_service.get_category_by_id(id, db)


@route.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=category_schema.Category,
    description="Create a new category"
)
def create_category(category: category_schema.CategoryBase, db: Session = Depends(get_db)):
    return category_service.create_category(category, db)


@route.put(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=category_schema.Category,
    description="Update a category"
)
def update_category(id: int, category: category_schema.CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(category, id, db)


@route.delete(
    "/categories/{id}",
    status_code=status.HTTP_200_OK,
    response_model=category_schema.Category,
    description="Delete a category"
)
def delete_category(id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(id, db)
