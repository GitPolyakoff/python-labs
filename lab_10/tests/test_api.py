import pytest
from app import app, repo

@pytest.fixture
def client():
    repo._db.clear()
    repo._next_id = 1
    with app.test_client() as client:
        yield client

def test_get_all_empty(client):
    res = client.get("/accounts")
    assert res.status_code == 200
    assert res.json == []

def test_create_account(client):
    data = {"client_name": "Иван", "currency": "RUB", "balance": 1000, "status": "active"}
    res = client.post("/accounts", json=data)
    assert res.status_code == 201
    assert res.json["id"] == 1
    assert res.json["client_name"] == "Иван"

def test_get_account_404(client):
    res = client.get("/accounts/999")
    assert res.status_code == 404
    assert res.json["code"] == "NOT_FOUND"

def test_delete_account(client):
    client.post("/accounts", json={"client_name": "А", "currency": "R", "balance": 0, "status": "active"})
    res = client.delete("/accounts/1")
    assert res.status_code == 204
    
    res2 = client.get("/accounts/1")
    assert res2.status_code == 404

def test_patch_account(client):
    client.post("/accounts", json={"client_name": "А", "currency": "R", "balance": 0, "status": "active"})
    res = client.patch("/accounts/1", json={"balance": 500})
    assert res.status_code == 200
    assert res.json["balance"] == 500

def test_create_invalid_balance(client):
    data = {"client_name": "Иван", "currency": "RUB", "balance": -500, "status": "active"}
    res = client.post("/accounts", json=data)
    assert res.status_code == 400
    assert res.json["code"] == "BAD_REQUEST"

def test_filter_by_status(client):
    client.post("/accounts", json={"client_name": "A", "currency": "R", "balance": 0, "status": "active"})
    client.post("/accounts", json={"client_name": "B", "currency": "R", "balance": 0, "status": "blocked"})
    
    res = client.get("/accounts?status=active")
    assert len(res.json) == 1
    assert res.json[0]["status"] == "active"

def test_special_operation_total_funds(client):
    client.post("/accounts", json={"client_name": "A", "currency": "R", "balance": 1000, "status": "active"})
    client.post("/accounts", json={"client_name": "B", "currency": "R", "balance": 500, "status": "active"})
    client.post("/accounts", json={"client_name": "C", "currency": "R", "balance": 2000, "status": "blocked"})
    
    res = client.get("/accounts/total-funds")
    assert res.status_code == 200
    assert res.json["total_active_funds"] == 1500