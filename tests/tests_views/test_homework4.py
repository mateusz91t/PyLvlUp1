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


@pytest.mark.parametrize(
    ['p_id', 'output', 's_code'],
    [
        [1, {"id": 1, "name": "Chai"}, 200],
        [63, {"id": 63, "name": 'Vegie-spread'}, 200],
        # ['avc', {"detail": "Id not found"}, 404],  # there is 422
        [9999, {"detail": "Id not found"}, 404],
        [-22, {"detail": "Id not found"}, 404],
        # [0.2, {"detail": "Id not found"}, 404],  # there is 422
    ]
)
def test_get_products(test_client, p_id, output, s_code):
    response = test_client.get(f"/products/{p_id}")
    assert response.status_code == s_code
    assert response.json() == output


@pytest.mark.parametrize(
    ['limit', 'offset', 'order', 's_code', 'output'],
    [
        [None, None, None, 200, {"id": 1, "last_name": "Davolio", "first_name": "Nancy", "city": "Seattle"}],
        [-10, -20, None, 200, {"id": 1, "last_name": "Davolio", "first_name": "Nancy", "city": "Seattle"}],
        [2, 1, None, 200, {"id": 1, "last_name": "Davolio", "first_name": "Nancy", "city": "Seattle"}],
        [None, None, ' ', 200, {"id": 1, "last_name": "Davolio", "first_name": "Nancy", "city": "Seattle"}],
        [None, None, 'abc', 400, {"detail": "Bad Request"}],
        [None, 3, 'first_name', 200, {"id": 8,	"last_name": "Callahan", "first_name": "Laura", "city": "Seattle"}],
        [None, 7, 'city', 200, {"id": 8,	"last_name": "Callahan", "first_name": "Laura", "city": "Seattle"}]
    ]
)
def test_get_employees(test_client, limit, offset, order, s_code, output):
    query = '?'
    if limit:
        query += f"{limit=}&"
    if offset:
        query += f"{offset=}&"
    if order:
        query += f"{order=}&"
    print(query)
    response = test_client.get(f"/employees{query}")

    assert response.status_code == s_code
    assert response.json()
