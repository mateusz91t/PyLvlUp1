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
        client.added_categories_ids = list()
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


@pytest.mark.parametrize(
    ['input', 's_code'],
    [
        [dict(name="test category"), 201],
        [dict(name="test category2"), 201],
        [dict(namex=""), 422]
    ]
)
def test_post_category(test_client, input, s_code):
    response = test_client.post("/categories", json=input)
    assert response.status_code == 201
    if s_code == 201:
        assert set(response.json().keys()) == {'id', 'name'}
        assert response.json()['name'] == input['name']
        test_client.added_categories_ids.append(response.json()['id'])


@pytest.mark.parametrize(
    ['id', 'input', 's_code'],
    [
        [test_client.added_categories_ids[0], dict(name="new test category"), 200],
        [test_client.added_categories_ids[1], dict(name="new test category2"), 200],
        [10, dict(namex=""), 422],
        [987456, dict(name="new test category3"), 404]
    ]
)
def test_put_category(test_client, id, input, s_code):
    response = test_client.put(f"/categories/{id}", json=input)
    assert response.status_code == 201
    if s_code in {200, 404}:
        assert set(response.json().keys()) == {'id', 'name'}
        assert response.json()['name'] == input['name']
        assert response.json()['id'] == id


def test_delete_category(test_client):
    for id in range(test_client.added_categories_ids[0], test_client.added_categories_ids[1] + 1):
        response = test_client.delete(f"/categories/{id}")
        assert response.status_code == 200
        assert response.json() == {"deleted": 1}
    response = test_client.delete(f"/categories/987654")
    assert response.status_code == 200
    assert response.json() == {"deleted": 0}
