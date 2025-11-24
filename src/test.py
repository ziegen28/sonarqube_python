from fastapi.testclient import TestClient
from main import app  # assuming your FastAPI code is in main.py

client = TestClient(app)

def test_add():
    response = client.get("/add", params={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 8}

def test_subtract():
    response = client.get("/subtract", params={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 2}

def test_multiply():
    response = client.get("/multiply", params={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 15}

def test_divide():
    response = client.get("/divide", params={"a": 6, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}

def test_divide_by_zero():
    response = client.get("/divide", params={"a": 6, "b": 0})
    assert response.status_code == 200
    assert response.json() == {"error": "Cannot divide by zero"}

def test_power():
    response = client.get("/power", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 8}

def test_modulo():
    response = client.get("/modulo", params={"a": 10, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 1}

def test_modulo_by_zero():
    response = client.get("/modulo", params={"a": 10, "b": 0})
    assert response.status_code == 200
    assert response.json() == {"error": "Cannot modulo by zero"}

def test_average():
    response = client.get("/average", params={"a": 4, "b": 6})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "swagger_url" in response.json()
