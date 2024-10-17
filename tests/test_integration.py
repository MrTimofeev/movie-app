import pytest
from fastapi.testclient import TestClient
from backend.app.main import app  # Замените на путь к вашему приложению

client = TestClient(app)

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_main_page():
    response = client.get("/")
    assert response.status_code == 200  # Проверка, что статус код 200
