import pytest
from fastapi.testclient import TestClient

from views.main import app


@pytest.yield_fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_get_categories(test_client):
    response = test_client.get("/categories")
    assert response.status_code == 200
    assert {"id": 1, "name": "Beverages"} in response.json()['categories']


def test_get_customers(test_client):
    response = test_client.get("/customers")
    assert response.status_code == 200
    assert {
               "id": "ALFKI",
               "name": "Alfreds Futterkiste",
               "full_address": "Obere Str. 57 12209 Berlin Germany",
           } in response.json()['customers']
