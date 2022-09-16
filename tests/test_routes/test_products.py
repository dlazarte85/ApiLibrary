import json

product_data_create = {
    "category_id": 1,
    "name": "Product Name",
    "price": 4499.99,
    "stock": 8,
    "enabled": True
}

category_data_create = {
    "name": "Category Name",
    "enabled": True
}


def test_get_product_return_ok(client, normal_user_token_headers):
    # Create a new category
    client.post("/api/categories", json.dumps(category_data_create), headers=normal_user_token_headers)
    # Create a new product
    client.post("/api/products", json.dumps(product_data_create), headers=normal_user_token_headers)
    # Test get product
    r = client.get('/api/products/1', headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 200
    assert response["data"]["name"] == "Product Name"


def test_create_product_return_ok(client, normal_user_token_headers):
    # Create a new category
    client.post("/api/categories", json.dumps(category_data_create), headers=normal_user_token_headers)
    # Create a new product
    r = client.post("/api/products", json.dumps(product_data_create), headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 201
    assert response["status"] == True
    assert response["data"]["name"] == "Product Name"
    assert response["data"]["price"] == 4499.99
    assert response["data"]["stock"] == 8
    assert response["data"]["enabled"] == True


def test_update_product_return_ok(client, normal_user_token_headers):
    # Create a new category
    client.post("/api/categories", json.dumps(category_data_create), headers=normal_user_token_headers)
    # Create a new product
    r = client.post("/api/products", data=json.dumps(product_data_create), headers=normal_user_token_headers)
    response = r.json()
    product_id = response['data']['id']
    data_update = {
        "name": "Product Update",
        "price": 4999.99,
        "stock": 18,
        "enabled": False,
    }
    r = client.put(f"/api/products/{product_id}", data=json.dumps(data_update), headers=normal_user_token_headers)
    response = r.json()
    assert r.status_code == 200
    assert response["data"]["name"] == "Product Update"
    assert response["data"]["price"] == 4999.99
    assert response["data"]["stock"] == 18
    assert response["data"]["enabled"] == False


def test_delete_product_return_ok(client, normal_user_token_headers):
    # Create a new category
    client.post("/api/categories", json.dumps(category_data_create), headers=normal_user_token_headers)
    # Create a new product
    r = client.post("/api/products", data=json.dumps(product_data_create), headers=normal_user_token_headers)
    response = r.json()
    product_id = response['data']['id']
    r = client.delete(f"/api/products/{product_id}", headers=normal_user_token_headers)
    response = r.json()
    assert response["data"]["deleted"] == True
