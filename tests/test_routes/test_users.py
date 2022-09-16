import json

data_create = {
    "username": "testuser",
    "name": "Test User",
    "email": "testuser@nofoobar.com",
    "enabled": True,
    "password": "pass_testing"
}


def test_get_user_return_ok(client, normal_user_token_headers):
    # Create a new user
    client.post("/api/users", json.dumps(data_create))
    # Test get user
    r = client.get('/api/users/1', headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 200
    assert response["data"]["username"] == "test@example.com"


def test_create_user_return_ok(client):
    r = client.post("/api/users", json.dumps(data_create))
    response = r.json()
    assert r.status_code == 201
    assert response["status"] == True
    assert response["data"]["username"] == "testuser"
    assert response["data"]["email"] == "testuser@nofoobar.com"
    assert response["data"]["enabled"] == True


def test_update_user_return_ok(client, normal_user_token_headers):
    # Create a new user
    r = client.post("/api/users", data=json.dumps(data_create))
    response = r.json()
    user_id = response['data']['id']
    data_update = {
        "username": "updateuser",
        "name": "Test Update",
        "email": "update@nofoobar.com",
        "enabled": False
    }
    r = client.put(f"/api/users/{user_id}", data=json.dumps(data_update), headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 200
    assert response["data"]["username"] == "updateuser"
    assert response["data"]["name"] == "Test Update"
    assert response["data"]["email"] == "update@nofoobar.com"
    assert response["data"]["enabled"] == False
