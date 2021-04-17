import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
client.counter = 0

# pytest -v -W ignore::DeprecationWarning
# -v wyświetli szczegółowe inf o testach
# -W pozwoli ukryć warningi wymienionego typu


def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello'}


@pytest.mark.parametrize('name', ['Zenek', 'Janek', 'Matt', '12312@! 1'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    # assert response.text == f'"Hello {name}"'  # refactor
    assert response.json() == {"message": f"Hello {name}"}


def test_counter():
    # 1st test
    response = client.get("/counter")
    assert response.status_code == 200
    assert response.text == '1'
    # 2nd test
    response = client.get("/counter")
    assert response.status_code == 200
    assert response.text == '2'


def test_method():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "options"}
