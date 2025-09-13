import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Paper Trading API" in response.json()["message"]

def test_place_trade():
    trade_data = {
        "symbol": "AAPL",
        "trade_type": "BUY",
        "quantity": 10,
        "price": 150.00
    }
    response = client.post("/api/v1/trades/", json=trade_data)
    # Note: This will fail without proper database setup
    # This is just to show the test structure

def test_get_portfolio():
    response = client.get("/api/v1/portfolio/")
    # Add assertions based on expected response

def test_get_positions():
    response = client.get("/api/v1/positions/")
    # Add assertions based on expected response
