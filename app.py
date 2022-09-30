from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException

from routes.user_route import route as user_route
from routes.auth_route import route as auth_route
from routes.category_route import route as category_route
from routes.product_route import route as product_route
import logging

logging.basicConfig(filename='./logs/api.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def catch_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    logging.error(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": False, "error": "An error has occurred, please try later"},
    )


@app.exception_handler(RequestValidationError)
async def catch_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:

    logging.error(exc)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": False, "error": jsonable_encoder(exc.errors())},
    )


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "error": exc.message}
    )

app.include_router(user_route)
app.include_router(auth_route)
app.include_router(category_route)
app.include_router(product_route)
