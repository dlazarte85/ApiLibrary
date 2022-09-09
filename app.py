from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routes.user_route import route as user_route
import logging

logging.basicConfig(filename='./logs/api.log', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()


@app.exception_handler(Exception)
async def catch_exception_handler(request: Request, exc: Exception):

    logging.error(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": False, "error": "An error has occurred, please try later"},
    )


app.include_router(user_route)
