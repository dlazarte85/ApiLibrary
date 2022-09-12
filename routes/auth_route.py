from schemas.token_schema import Token
from service import auth_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from fastapi.security import OAuth2PasswordRequestForm


route = APIRouter(prefix="/api")


@route.post(
    "/login",
    tags=["auth"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = await auth_service.generate_token(form_data.username, form_data.password, db)
    return Token(access_token=access_token, token_type="bearer")
