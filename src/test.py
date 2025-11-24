from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Helper for invalid params ---
def call_endpoint(path, params):
    return client.get(path, params=params)

# --- Arithmetic endpoint tests ---
def test_add():
    assert call_endpoint("/add", {"a": 5, "b": 3}).json() == {"result": 8}
    # Edge case: negative numbers
    assert call_endpoint("/add", {"a": -2, "b": 3}).json() == {"result": 1}
    # Edge case: floats
    assert call_endpoint("/add", {"a": 2.5, "b": 3.5}).json() == {"result": 6.0}

def test_subtract():
    assert call_endpoint("/subtract", {"a": 5, "b": 3}).json() == {"result": 2}
    assert call_endpoint("/subtract", {"a": 3, "b": 5}).json() == {"result": -2}

def test_multiply():
    assert call_endpoint("/multiply", {"a": 5, "b": 3}).json() == {"result": 15}
    assert call_endpoint("/multiply", {"a": -2, "b": 4}).json() == {"result": -8}

def test_divide():
    assert call_endpoint("/divide", {"a": 6, "b": 3}).json() == {"result": 2.0}
    assert call_endpoint("/divide", {"a": 5, "b": 2}).json() == {"result": 2.5}
    # Divide by zero
    assert call_endpoint("/divide", {"a": 6, "b": 0}).json() == {"error": "Cannot divide by zero"}

def test_power():
    assert call_endpoint("/power", {"a": 2, "b": 3}).json() == {"result": 8}
    assert call_endpoint("/power", {"a": 2, "b": 0}).json() == {"result": 1}

def test_modulo():
    assert call_endpoint("/modulo", {"a": 10, "b": 3}).json() == {"result": 1}
    assert call_endpoint("/modulo", {"a": 10, "b": 0}).json() == {"error": "Cannot modulo by zero"}

def test_average():
    assert call_endpoint("/average", {"a": 4, "b": 6}).json() == {"result": 5.0}
    # Edge cases
    assert call_endpoint("/average", {"a": 0, "b": 0}).json() == {"result": 0.0}
    assert call_endpoint("/average", {"a": -4, "b": 4}).json() == {"result": 0.0}

def test_home():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert "swagger_url" in data

# --- Optional: test invalid input types for better coverage ---
def test_invalid_inputs():
    endpoints = ["/add", "/subtract", "/multiply", "/divide", "/power", "/modulo", "/average"]
    for ep in endpoints:
        response = call_endpoint(ep, {"a": "x", "b": "y"})
        assert response.status_code == 422  # FastAPI validation error


