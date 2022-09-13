from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(data: dict, code=status.HTTP_200_OK) -> JSONResponse:
    data = jsonable_encoder(data, exclude={"password"})
    api_response = jsonable_encoder({"status": True, "data": data})
    return JSONResponse(content=api_response, status_code=code)


def error_response(message: str, code) -> JSONResponse:
    api_response = jsonable_encoder({"status": False, "error": message})
    return JSONResponse(content=api_response, status_code=code)
