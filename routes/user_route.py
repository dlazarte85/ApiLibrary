from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from config.db import get_db
from schemas import user_schema
from service import user_service
from service import auth_service

route = APIRouter(prefix="/api", tags=["users"])


@route.get(
    "/users",
    response_model=list[user_schema.User],
    status_code=status.HTTP_200_OK,
    description="Show all users"
)
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@route.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.User,
    description="Return logged in user"
)
async def read_users_me(current_user: user_schema.User = Depends(auth_service.get_current_user)):
    return current_user


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


@route.put(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.User,
    description="Update a user"
)
async def update_user(id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(user, id, db)


@route.delete(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.User,
    description="Delete a user"
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(id, db)
