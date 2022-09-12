import json

data_create = {
    "username": "testuser",
    "name": "Test User",
    "email": "testuser@nofoobar.com",
    "enabled": True,
    "password": "pass_testing"
}


def test_get_user(client):
    # Create a new user
    client.post("/api/users", json.dumps(data_create))
    # Test get user
    response = client.get('/api/users/1')
    assert response.status_code == 200


def test_create_user(client):
    response = client.post("/api/users", json.dumps(data_create))
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["enabled"] == True


def test_update_user(client):
    # Create a new user
    client.post("/api/users", json.dumps(data_create))
    data_update = {
        "username": "updateuser",
        "name": "Test Update",
        "email": "update@nofoobar.com",
        "enabled": False
    }
    client.put("/api/users/1", json.dumps(data_update))
    response = client.put("/api/users/1", json.dumps(data_update))
    assert response.status_code == 200
    assert response.json()["username"] == "updateuser"
    assert response.json()["name"] == "Test Update"
    assert response.json()["email"] == "update@nofoobar.com"
    assert response.json()["enabled"] == False
