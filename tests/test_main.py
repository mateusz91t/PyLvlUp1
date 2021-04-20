import datetime

import pytest
from fastapi.testclient import TestClient

from main import app
from myservices.methods_for_main import get_hash

client = TestClient(app)
client.counter = 0

# pytest -v -W ignore::DeprecationWarning
# -v wyświetli szczegółowe inf o testach
# -W pozwoli ukryć warningi wymienionego typu

today = datetime.date.today()
json_to_register = {
    "name": "Jan",
    "surname": "Kowalski-Żądło"
}
json_registered = {
    "id": 1,
    "name": "Jan",
    "surname": "Kowalski-Żądło",
    "register_date": str(today),
    "vaccination_date": str(today + datetime.timedelta(16))
}


def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world!'}


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


def test_method_options():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


def test_method_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_method_delete():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


def test_method_put():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_method_post():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}


@pytest.mark.parametrize(
    ['password', 'password_hash', 'result'],
    [
        ['abc', get_hash('abc'), 204],
        ['haslo', 'zahaszowane_haslo', 401],
        ['', '', 401],
        ['', 'cos', 401],
        ['cos', '', 401]
    ]
)
def test_auth(password: str, password_hash: str, result: int):
    response = client.get(f"/auth?password={password}&password_hash={password_hash}")
    assert response.status_code == result
    if result == 204:
        assert not response.content


@pytest.mark.parametrize(
    [  # values set
        'json_in', 'json_out'
    ],
    [  # answers set
        [  # 1st answer
            json_to_register,  # 1st element [json_in] from 1st answer
            json_registered  # 2nd element [json_out] from 1st answer
        ]
    ]
)
def test_register_view(json_in, json_out):
    response = client.post(f"/register", json=json_in)
    dct_json = dict(response.json())
    assert response.status_code == 201
    assert dct_json['name'] == json_out['name']
    assert dct_json['surname'] == json_out['surname']


@pytest.fixture
def set_patient():
    response = client.post("/register", json=json_to_register)


@pytest.mark.parametrize(
    ['ide', 'result', 'body'],
    [
        [1, 200, json_registered],
        [123123, 404, 'not found your patient id'],
        [-2, 400, 'id cannot be lower than 0']
    ]
)
def test_patient_view(ide, result, body, set_patient):
    response = client.get(f"/patient/{ide}")
    assert response.status_code == result
    assert response.json() == body
