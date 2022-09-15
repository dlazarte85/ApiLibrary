import threading
import time

from schemas import product_schema
from schemas.generic_response_schema import GenericResponse, GenericErrorResponse
from service import product_service, auth_service
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db, session_scope
from utils import api_response
from multiprocessing import Process

route = APIRouter(prefix="/api",
                  dependencies=[Depends(auth_service.get_current_user)],
                  responses={422: {"model": GenericErrorResponse}},
                  tags=["products"])


@route.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[list[product_schema.Product]],
    description="Show all products"
)
async def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    products = product_service.get_products(db, skip, limit)
    return api_response.success_response(products)


@route.get(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Show a product"
)
async def get_product(id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.get_product_by_id(id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=GenericResponse[product_schema.Product],
    description="Create a new product"
)
async def create_product(product: product_schema.ProductCreate, db: Session = Depends(session_scope())):
    try:
        product = product_service.create_product(product, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.put(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Update a product"
)
async def update_product(id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    try:
        product = product_service.update_product(product, id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.delete(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse[product_schema.Product],
    description="Delete a product"
)
async def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.delete_product(id, db)
        return api_response.success_response(product)
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/products/seed_products",
    status_code=status.HTTP_200_OK,
    description="Seed a product"
)
async def seed_products(db: Session = Depends(get_db)):
    try:
        time_start = time.time()
        amount = 50000
        response = product_service.seed_products(amount, db)
        time_end = time.time() - time_start
        response["time"] = time_end
        return response
    except HTTPException as e:
        return api_response.error_response(e.detail, e.status_code)


@route.post(
    "/products/seed_products_threading/{n_threads}",
    status_code=status.HTTP_200_OK,
    description="Seed a product"
)
async def seed_products_threading(n_threads: int):
    time_start = time.time()
    threads = []
    amount = 50000 // n_threads
    print(amount)
    for i in range(n_threads):
        t = threading.Thread(target=product_service.seed_products_thread_process, args=(amount,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    time_duration = time.time() - time_start
    response = {"message": "Products created successfully", "time": time_duration}
    return response


@route.post(
    "/products/seed_products_multipr/{n_threads}",
    status_code=status.HTTP_200_OK,
    description="Seed a product"
)
async def seed_products_multipr(n_threads: int):
    time_start = time.time()
    process = []
    amount = 50000 // n_threads
    print(amount)
    for i in range(n_threads):
        p = Process(target=product_service.seed_products_thread_process, args=(amount,))
        process.append(p)
        p.start()

    for p in process:
        p.join()

    time_duration = time.time() - time_start
    response = {"message": "Products created successfully", "time": time_duration}
    return response
