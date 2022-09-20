from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str | None = None
    name: str | None = None
    email: EmailStr | None = None
    enabled: bool | None = None
    is_admin: bool | None = False


class UserCreate(UserBase):
    username: str
    name: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "example",
                "name": "Example Name",
                "email": "email@example.com",
                "is_admin": 1,
                "enabled": 1,
            }
        }
