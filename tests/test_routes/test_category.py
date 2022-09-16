import json

data_create = {
    "name": "Category Name",
    "enabled": True
}


def test_get_category_return_ok(client, normal_user_token_headers):
    # Create a new category
    client.post("/api/categories", json.dumps(data_create), headers=normal_user_token_headers)
    # Test get category
    r = client.get('/api/categories/1', headers=normal_user_token_headers)
    response = r.json()
    print(response)
    assert r.status_code == 200
    assert response["status"] == True
    assert response["data"]["name"] == "Category Name"


def test_create_category_return_ok(client, normal_user_token_headers):
    r = client.post("/api/categories", json.dumps(data_create), headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 201
    assert response["status"] == True
    assert response["data"]["name"] == "Category Name"
    assert response["data"]["enabled"] == True


def test_update_category_return_ok(client, normal_user_token_headers):
    # Create a new user
    r = client.post("/api/categories", data=json.dumps(data_create), headers=normal_user_token_headers)
    response = r.json()
    category_id = response['data']['id']
    data_update = {
        "name": "Category Update",
        "enabled": False,
    }
    r = client.put(f"/api/categories/{category_id}", data=json.dumps(data_update), headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 200
    assert response["status"] == True
    assert response["data"]["name"] == "Category Update"
    assert response["data"]["enabled"] == False


def test_delete_category_return_ok(client, normal_user_token_headers):
    # Create a new user
    r = client.post("/api/categories", data=json.dumps(data_create), headers=normal_user_token_headers)
    response = r.json()
    category_id = response['data']['id']
    r = client.delete(f"/api/categories/{category_id}", headers=normal_user_token_headers)
    response = r.json()
    assert response["status"] == True
    assert response["data"]["name"] == "Category Name"
