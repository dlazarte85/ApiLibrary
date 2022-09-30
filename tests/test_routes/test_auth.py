import json
from unittest import TestCase

from tests.utils.db_objects import user_data_create


def test_login_return_ok(client):
    # Create a new user
    client.post("/api/users", json.dumps(user_data_create))
    # Test login
    data = {"username": "testuser", "password": "pass_testing"}
    r = client.post('/api/login', json.dumps(data))
    response = r.json()
    assert r.status_code == 200
    assert response['status']
    assert response['data']['token_type'] == 'bearer'
