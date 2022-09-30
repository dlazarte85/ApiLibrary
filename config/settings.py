import os

from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):

    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')

    database_url: str = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    jwt_secret_key: str = os.getenv('SECRET_KEY')
    jwt_access_token_expires_in: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    jwt_refresh_token_expires_in: int = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

    test_user_email = str = os.getenv('TEST_USER_EMAIL')


settings = Settings()
