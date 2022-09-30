import json

from service.user_service import create_user, get_user_by_email
from fastapi.testclient import TestClient
from schemas.user_schema import UserCreate
from sqlalchemy.orm import Session


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/api/login", json.dumps(data))
    response = r.json()
    access_token = response["data"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    name = "Test"
    user = get_user_by_email(email=email, db=db)
    if not user:
        user_in_create = UserCreate(username=email, name=name, email=email, password=password, password_confirm=password)
        user = create_user(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
