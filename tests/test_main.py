import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# pytest -v -W ignore::DeprecationWarning
# -v wyświetli szczegółowe inf o testach
# -W pozwoli ukryć warningi wymienionego typu


def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello'}


@pytest.mark.parametrize('name', ['Zenek', 'Janek', 'Matt', '12312@! 1'])
def test_hello_name(name):
    # name = "Matt"
    response = client.get(f"/hello/{name}")
    print('jajajajaja')
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'
