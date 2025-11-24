from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# --- All endpoints ---
endpoints = ["/add", "/subtract", "/multiply", "/divide", "/power", "/modulo", "/average"]

# --- Happy paths and edge cases ---
@pytest.mark.parametrize("endpoint", endpoints)
@pytest.mark.parametrize("a,b", [
    (5, 3),
    (0, 0),
    (-5, 3),
    (2.5, 3.5),
    (999999, 1),
])
def test_happy_and_edge_cases(endpoint, a, b):
    # Skip divide/modulo zero for now, handled separately
    if endpoint == "/divide" and b == 0:
        pytest.skip("Skip divide by zero here")
    if endpoint == "/modulo" and b == 0:
        pytest.skip("Skip modulo by zero here")
    response = client.get(endpoint, params={"a": a, "b": b})
    assert response.status_code == 200
    json_data = response.json()
    assert "result" in json_data or "error" in json_data

# --- Divide / modulo by zero ---
@pytest.mark.parametrize("endpoint", ["/divide", "/modulo"])
def test_zero_division(endpoint):
    response = client.get(endpoint, params={"a": 5, "b": 0})
    assert response.status_code == 200
    assert "error" in response.json()

# --- Invalid types ---
@pytest.mark.parametrize("endpoint", endpoints)
@pytest.mark.parametrize("a,b", [
    ("x", 1),
    (1, "y"),
    ("x", "y"),
    (None, 1),
    (1, None),
    ("", 1),
    (1, ""),
])
def test_invalid_types(endpoint, a, b):
    response = client.get(endpoint, params={"a": a, "b": b})
    assert response.status_code == 422

# --- Missing parameters ---
@pytest.mark.parametrize("endpoint", endpoints)
def test_missing_parameters(endpoint):
    response = client.get(endpoint, params={"a": 5})
    assert response.status_code == 422
    response = client.get(endpoint, params={"b": 5})
    assert response.status_code == 422
    response = client.get(endpoint, params={})
    assert response.status_code == 422

# --- Home endpoint ---
def test_home():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert "swagger_url" in data
