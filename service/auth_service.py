from config.oauth2 import AuthJWT
from sqlalchemy.orm import Session
from datetime import timedelta

from fastapi import Depends, HTTPException, status

from passlib.context import CryptContext

from schemas.token_schema import TokenData
from config.settings import settings
from config.db import get_db
from service import user_service

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_IN = settings.jwt_access_token_expires_in
REFRESH_TOKEN_EXPIRES_IN = settings.jwt_refresh_token_expires_in

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db: Session):
    user = user_service.get_user(username, db)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if not verify_password(password, user.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect password")
    return user


async def generate_token(username: str, password: str, authorize: AuthJWT, db: Session):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)

    access_token = authorize.create_access_token(subject=username, expires_time=access_token_expires)
    refresh_token = authorize.create_refresh_token(subject=username, expires_time=refresh_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token}


class UserNotFound(Exception):
    pass


async def get_current_user(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        token_data = TokenData(username=username)
        user = user_service.get_user(username=token_data.username, db=db)
        if user is None:
            raise UserNotFound('User no longer exists')

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')

    return user


async def refresh_access_token(authorize: AuthJWT, db: Session):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    try:
        authorize.jwt_refresh_token_required()

        current_user = authorize.get_jwt_subject()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not refresh access token')
        user = user_service.get_user(username=current_user, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='The user belonging to this token no logger exist')

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
        new_access_token = authorize.create_access_token(subject=current_user, expires_time=access_token_expires)
        return {"access_token": new_access_token}
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

