from fastapi import APIRouter, status

route = APIRouter(prefix="/api", tags=["users"])


@route.get(
    "/users",
    status_code=status.HTTP_200_OK,
)
async def get_users():
    return {"msg": "Endpoint get users"}
