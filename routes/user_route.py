from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from config.db import get_db
from schemas import user_schema
from service import user_service

route = APIRouter(prefix="/api", tags=["users"])


@route.get(
    "/users",
    response_model=list[user_schema.User],
    status_code=status.HTTP_200_OK,
)
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@route.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.User,
    description="Show a user"
)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(id, db)


@route.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    description="Create a new user"
)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)
