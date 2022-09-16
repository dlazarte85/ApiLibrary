import os

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from config.db import session_scope
from models.product_model import ProductModel
from schemas import product_schema
from service import category_service

import string
import random


def get_product(db: Session, text: str):
    return db.query(ProductModel).filter(ProductModel.name.like(f'%{text}%')).first()


def get_product_by_id(product_id: int, db: Session):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product


def get_product_by_name(name: str, db: Session, product_id: int = None):
    all_filters = [ProductModel.name == name]
    if product_id is not None:
        all_filters.append(ProductModel.id != product_id)
    return db.query(ProductModel).filter(*all_filters).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductModel).offset(skip).limit(limit).all()


def create_product(product: product_schema.ProductCreate, db: Session):
    if get_product_by_name(product.name, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product name already exists")

    db_category = category_service.get_category_by_id(product.category_id, db)

    db_product = ProductModel(
        category_id=db_category.id,
        name=product.name,
        price=product.price,
        stock=product.stock,
        enabled=product.enabled
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(product: product_schema.ProductUpdate, product_id: int, db: Session):
    db_product = get_product_by_id(product_id, db)

    if get_product_by_name(product.name, db, product_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product name already exists")

    if product.category_id:
        category_service.get_category_by_id(product.category_id, db)

    db.query(ProductModel).filter(ProductModel.id == product_id)\
        .update(product.dict(exclude_none=True))
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(product_id: int, db: Session):
    db_product = get_product_by_id(product_id, db)
    db_product.deleted = True

    db.commit()
    db.refresh(db_product)
    return db_product


def seed_products(n_records: int, db: Session):
    for i in range(n_records):
        name = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(10, 15)))
        price = ''.join(random.choice(string.digits) for i in range(4))
        stock = ''.join(random.choice(string.digits) for i in range(2))
        data = {
            "category_id": 1,
            "name": name,
            "price": price,
            "stock": stock,
            "enabled": True
        }
        db_product = ProductModel(**data)
        db.add(db_product)

    db.commit()
    return {"message": "Products created successfully"}


def seed_products_thread_process(amount: int):
    with session_scope() as s:
        for i in range(amount):
            name = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(10, 15)))
            price = ''.join(random.choice(string.digits) for i in range(4))
            stock = ''.join(random.choice(string.digits) for i in range(2))
            data = {
                "category_id": 1,
                "name": name,
                "price": price,
                "stock": stock,
                "enabled": True
            }
            db_product = ProductModel(**data)
            s.add(db_product)

    print(f"Process Id: {os.getpid()}")
    return {"message": "Products created successfully"}
