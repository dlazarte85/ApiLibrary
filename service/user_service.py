from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from models.user_model import UserModel
from schemas import user_schema
from service.auth_service import get_password_hash


def get_user(username: str, db: Session):
    return db.query(UserModel).filter(
        (UserModel.username == username) | (UserModel.email == username)
    ).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user_by_id(user_id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return db_user


def get_user_by_email(db: Session, email: str, user_id: int = None):
    all_filters = [UserModel.email == email]
    if user_id is not None:
        all_filters.append(UserModel.id != user_id)
    db_user = db.query(UserModel).filter(*all_filters).first()
    return db_user


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


def update_user(user: user_schema.UserUpdate, user_id: int, db: Session):
    if get_user_by_email(db, user.email, user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user.password = get_password_hash(user.password)
    db.query(UserModel).filter(UserModel.id == user_id)\
        .update(user.dict(exclude_none=True))
    db.commit()
    db_user = get_user_by_id(user_id, db)
    return db_user


def delete_user(user_id: int, db: Session):
    db_user = get_user_by_id(user_id, db)

    db.delete(db_user)
    db.commit()
    return db_user
