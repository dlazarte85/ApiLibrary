from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.category_model import CategoryModel
from schemas import category_schema


def get_category(db: Session, text: str):
    return db.query(CategoryModel).filter(CategoryModel.name.like(f'%{text}%')).first()


def get_category_by_id(category_id: int, db: Session):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category


def get_category_by_name(name: str, db: Session, category_id: int = None):
    all_filters = [CategoryModel.name == name]
    if category_id is not None:
        all_filters.append(CategoryModel.id != category_id)
    return db.query(CategoryModel).filter(*all_filters).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CategoryModel).offset(skip).limit(limit).all()


def create_category(category: category_schema.CategoryBase, db: Session):
    if get_category_by_name(category.name, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")

    db_category = CategoryModel(
        name=category.name,
        enabled=category.enabled,
        deleted=category.deleted
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(category: category_schema.CategoryUpdate, category_id: int, db: Session):
    db_category = get_category_by_id(category_id, db)

    if get_category_by_name(category.name, db, category_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")

    db.query(CategoryModel).filter(CategoryModel.id == category_id)\
        .update(category.dict(exclude_none=True))
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(category_id: int, db: Session):
    db_category = get_category_by_id(category_id, db)
    db.delete(db_category)
    db.commit()
    return db_category
