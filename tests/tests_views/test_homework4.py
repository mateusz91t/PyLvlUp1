import pytest
from fastapi.testclient import TestClient

from views.main import app


# to run all tests type in terminal:
# pytest
# to run custom method by fragment of name:
# pytest -svk employee


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
        # ['avc', {"detail": "Id not found"}, 404],
        [9999, {"detail": "Id not found"}, 404],
        [-22, {"detail": "Id not found"}, 404],
        # [0.2, {"detail": "Id not found"}, 404],
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
        [2, 1, None, 200, {"id": 2, "last_name": "Fuller", "first_name": "Andrew", "city": "Tacoma"}],
        [None, None, ' ', 200, {"id": 1, "last_name": "Davolio", "first_name": "Nancy", "city": "Seattle"}],
        [None, None, 'abc', 400, {"detail": "Bad Request"}],
        [None, 3, 'first_name', 200, {"id": 8, "last_name": "Callahan", "first_name": "Laura", "city": "Seattle"}],
        [None, 7, 'city', 200, {"id": 8, "last_name": "Callahan", "first_name": "Laura", "city": "Seattle"}]
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
    response = test_client.get("/employees", params=dict(limit=limit, offset=offset, order=order))

    assert response.status_code == s_code
    if s_code == 200:
        assert output in response.json()['employees']
    else:
        assert output == response.json()


def test_get_products_extended(test_client):
    """The test check a status code, an output item and sorting"""
    response = test_client.get("/products_extended")
    assert response.status_code == 200  # status
    assert {  # output item
               "id": 1,
               "name": "Chai",
               "category": "Beverages",
               "supplier": "Exotic Liquids",
           } in response.json()["products_extended"]
    # and sorting
    assert response.json()["products_extended"][0]['id'] < response.json()["products_extended"][1]['id']
    assert response.json()["products_extended"][-2]['id'] < response.json()["products_extended"][-1]['id']


@pytest.mark.parametrize(
    ['id', 's_code', 'output'],
    [
        [10, 200, {"id": 10273, "customer": "QUICK-Stop", "quantity": 24, "total_price": 565.44}],
        [1234567, 404, {"detail": "Id not found"}]
    ]
)
def test_get_orders_by_id_product(test_client, id, s_code, output):
    response = test_client.get(f"/products/{id}/orders")
    assert response.status_code == s_code
    if s_code == 200:
        assert output in response.json()['orders']
    else:
        assert output == response.json()
