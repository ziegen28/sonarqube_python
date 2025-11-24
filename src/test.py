from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# --- Helper to call endpoints ---
def call(ep, a=None, b=None):
    params = {}
    if a is not None:
        params["a"] = a
    if b is not None:
        params["b"] = b
    return client.get(ep, params=params)

# --- Arithmetic happy paths and edge cases ---
@pytest.mark.parametrize("endpoint,a,b,expected", [
    ("/add", 5, 3, {"result": 8}),
    ("/add", -2, 3, {"result": 1}),
    ("/add", 2.5, 3.5, {"result": 6.0}),
    
    ("/subtract", 5, 3, {"result": 2}),
    ("/subtract", 3, 5, {"result": -2}),
    
    ("/multiply", 5, 3, {"result": 15}),
    ("/multiply", -2, 4, {"result": -8}),
    
    ("/divide", 6, 3, {"result": 2.0}),
    ("/divide", 5, 2, {"result": 2.5}),
    
    ("/power", 2, 3, {"result": 8}),
    ("/power", 2, 0, {"result": 1}),
    
    ("/modulo", 10, 3, {"result": 1}),
    
    ("/average", 4, 6, {"result": 5.0}),
    ("/average", 0, 0, {"result": 0.0}),
    ("/average", -4, 4, {"result": 0.0}),
])
def test_happy_paths(endpoint, a, b, expected):
    response = call(endpoint, a, b)
    assert response.status_code == 200
    assert response.json() == expected

# --- Divide / modulo by zero ---
@pytest.mark.parametrize("endpoint,a,b,expected", [
    ("/divide", 6, 0, {"error": "Cannot divide by zero"}),
    ("/modulo", 10, 0, {"error": "Cannot modulo by zero"}),
])
def test_zero_division(endpoint, a, b, expected):
    response = call(endpoint, a, b)
    assert response.status_code == 200
    assert response.json() == expected

# --- Invalid input types (trigger FastAPI 422) ---
@pytest.mark.parametrize("endpoint,a,b", [
    ("/add", "x", 3),
    ("/subtract", 5, "y"),
    ("/multiply", "x", "y"),
    ("/divide", "a", "b"),
    ("/power", "x", "y"),
    ("/modulo", "x", "y"),
    ("/average", "x", "y"),
])
def test_invalid_types(endpoint, a, b):
    response = call(endpoint, a, b)
    assert response.status_code == 422

# --- Missing parameters (trigger FastAPI 422) ---
@pytest.mark.parametrize("endpoint,params", [
    ("/add", {"a": 5}),          # missing b
    ("/subtract", {"b": 3}),     # missing a
    ("/multiply", {}),           # missing both
])
def test_missing_params(endpoint, params):
    response = client.get(endpoint, params=params)
    assert response.status_code == 422

# --- Home endpoint ---
def test_home():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert "swagger_url" in data
