from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    username: str | None = None
    name: str | None = None
    email: EmailStr | None = None
    enabled: bool | None = None
    is_admin: bool | None = False
    password: str | None = None
    password_confirm: str | None = None

    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserCreate(UserBase):
    username: str
    name: str
    email: EmailStr
    password: str
    password_confirm: str


class UserUpdate(UserBase):
    pass


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
