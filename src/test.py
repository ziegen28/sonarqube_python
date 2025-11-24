from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Helper for requests ---
def call_get(endpoint, a=None, b=None):
    params = {}
    if a is not None:
        params["a"] = a
    if b is not None:
        params["b"] = b
    return client.get(endpoint, params=params)

# --- Happy path tests ---
def test_add_happy():
    assert call_get("/add", 5, 3).json() == {"result": 8}
    assert call_get("/add", -2, 3).json() == {"result": 1}
    assert call_get("/add", 2.5, 3.5).json() == {"result": 6.0}

def test_subtract_happy():
    assert call_get("/subtract", 5, 3).json() == {"result": 2}
    assert call_get("/subtract", 3, 5).json() == {"result": -2}

def test_multiply_happy():
    assert call_get("/multiply", 5, 3).json() == {"result": 15}
    assert call_get("/multiply", -2, 4).json() == {"result": -8}

def test_divide_happy():
    assert call_get("/divide", 6, 3).json() == {"result": 2.0}
    assert call_get("/divide", 5, 2).json() == {"result": 2.5}

def test_power_happy():
    assert call_get("/power", 2, 3).json() == {"result": 8}
    assert call_get("/power", 2, 0).json() == {"result": 1}

def test_modulo_happy():
    assert call_get("/modulo", 10, 3).json() == {"result": 1}

def test_average_happy():
    assert call_get("/average", 4, 6).json() == {"result": 5.0}
    assert call_get("/average", 0, 0).json() == {"result": 0.0}
    assert call_get("/average", -4, 4).json() == {"result": 0.0}

# --- Error conditions ---
def test_divide_by_zero():
    assert call_get("/divide", 6, 0).json() == {"error": "Cannot divide by zero"}

def test_modulo_by_zero():
    assert call_get("/modulo", 10, 0).json() == {"error": "Cannot modulo by zero"}

# --- Invalid input types (FastAPI 422) ---
def test_invalid_inputs():
    endpoints = ["/add", "/subtract", "/multiply", "/divide", "/power", "/modulo", "/average"]
    for ep in endpoints:
        response = call_get(ep, "x", "y")
        assert response.status_code == 422  # validation error

# --- Home endpoint ---
def test_home():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert "swagger_url" in data

