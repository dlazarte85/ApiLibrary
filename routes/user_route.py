from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from config.db import get_db
from schemas import user_schema
from schemas.generic_response_schema import GenericResponse, GenericErrorResponse
from service import user_service
from service import auth_service
from utils import api_response

route = APIRouter(prefix="/api",
                  responses={422: {"model": GenericErrorResponse}},
                  tags=["users"],)


@route.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[list[user_schema.User]],
    dependencies=[Depends(auth_service.get_current_user)],
    description="Show all users"
)
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return api_response.success_response(users)


@route.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[user_schema.User],
    description="Return logged in user"
)
async def read_users_me(current_user: user_schema.User = Depends(auth_service.get_current_user)):
    return api_response.success_response(current_user.__dict__)


@route.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[user_schema.User],
    dependencies=[Depends(auth_service.get_current_user)],
    description="Show a user"
)
async def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user_by_id(id, db)
        return api_response.success_response(user)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=GenericResponse[user_schema.User],
    description="Create a new user"
)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.create_user(user, db)
        return api_response.success_response(user, code=status.HTTP_201_CREATED)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.put(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[user_schema.User],
    dependencies=[Depends(auth_service.get_current_user)],
    description="Update a user"
)
async def update_user(id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    try:
        user = user_service.update_user(user, id, db)
        return api_response.success_response(user)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.delete(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[user_schema.User],
    dependencies=[Depends(auth_service.get_current_user)],
    description="Delete a user"
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.delete_user(id, db)
        return api_response.success_response(user)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)
