from schemas.generic_response_schema import GenericResponse, GenericErrorResponse
from schemas.token_schema import Token
from schemas.user_schema import UserLogin
from service import auth_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from config.oauth2 import AuthJWT
from utils import api_response

route = APIRouter(prefix="/api")


@route.post(
    "/login",
    tags=["auth"],
    response_model=GenericResponse[Token],
    responses={422: {"model": GenericErrorResponse}},
)
async def login_for_access_token(user: UserLogin, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        token = await auth_service.generate_token(user.username, user.password, authorize, db)
        token_response = Token(access_token=token['access_token'], refresh_token=token['refresh_token'], token_type="bearer")
        return api_response.success_response(token_response.__dict__)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post('/refresh')
async def refresh_access_token(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        access_token = await auth_service.refresh_access_token(authorize, db)
        return api_response.success_response(access_token)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)
