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

# --- Endpoint happy paths and edge cases ---
@pytest.mark.parametrize("endpoint,a,b,expected", [
    # add
    ("/add", 5, 3, {"result": 8}),
    ("/add", -2, 3, {"result": 1}),
    ("/add", 2.5, 3.5, {"result": 6.0}),
    ("/add", 0, 0, {"result": 0}),
    
    # subtract
    ("/subtract", 5, 3, {"result": 2}),
    ("/subtract", 3, 5, {"result": -2}),
    ("/subtract", 0, 0, {"result": 0}),
    
    # multiply
    ("/multiply", 5, 3, {"result": 15}),
    ("/multiply", -2, 4, {"result": -8}),
    ("/multiply", 0, 5, {"result": 0}),
    
    # divide
    ("/divide", 6, 3, {"result": 2.0}),
    ("/divide", 5, 2, {"result": 2.5}),
    
    # power
    ("/power", 2, 3, {"result": 8}),
    ("/power", 2, 0, {"result": 1}),
    
    # modulo
    ("/modulo", 10, 3, {"result": 1}),
    
    # average
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

# --- Invalid input types (FastAPI 422) ---
@pytest.mark.parametrize("endpoint,a,b", [
    ("/add", "x", 3),
    ("/add", 5, "y"),
    ("/subtract", "x", 3),
    ("/subtract", 5, "y"),
    ("/multiply", "x", 3),
    ("/multiply", 5, "y"),
    ("/divide", "x", 3),
    ("/divide", 5, "y"),
    ("/power", "x", 3),
    ("/power", 5, "y"),
    ("/modulo", "x", 3),
    ("/modulo", 5, "y"),
    ("/average", "x", 3),
    ("/average", 5, "y"),
])
def test_invalid_types(endpoint, a, b):
    response = call(endpoint, a, b)
    assert response.status_code == 422  # FastAPI validation error

# --- Missing parameters (FastAPI 422) ---
@pytest.mark.parametrize("endpoint,params", [
    ("/add", {"a": 5}),          # missing b
    ("/add", {"b": 3}),          # missing a
    ("/subtract", {"a": 5}),     
    ("/subtract", {"b": 3}),
    ("/multiply", {"a": 5}),
    ("/multiply", {"b": 3}),
    ("/divide", {"a": 5}),
    ("/divide", {"b": 3}),
    ("/power", {"a": 5}),
    ("/power", {"b": 3}),
    ("/modulo", {"a": 5}),
    ("/modulo", {"b": 3}),
    ("/average", {"a": 5}),
    ("/average", {"b": 3}),
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
