from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from config.settings import settings


# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = settings.jwt_secret_key


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()
