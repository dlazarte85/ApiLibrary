from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from models.user_model import UserModel
from schemas import user_schema
from service.auth_service import get_password_hash


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user_by_id(user_id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return db_user


def get_user_by_email(db: Session, email: str, user_id: int = None):
    db_user = db.query(UserModel).filter(UserModel.email == email)
    if user_id is not None:
        db_user.filter(UserModel.id == user_id)
    return db_user.first()


def create_user(user: user_schema.UserCreate, db: Session):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = UserModel(
        username=user.username,
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        enabled=user.enabled
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
