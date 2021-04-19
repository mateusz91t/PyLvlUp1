import pytest
from fastapi.testclient import TestClient

from main import app
from myservices.methods_for_main import get_hash

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


@pytest.mark.parametrize(
    ['password', 'password_hash'],
    [
        ['abc', get_hash('abc')],
        ['haslo', 'zahaszowane_haslo']
    ]
)
def test_auth(password: str, password_hash: str):
    response = client.get(f"/auth?password={password}&password_hash={password_hash}")
    if password_hash == get_hash(password):
        assert response.status_code == 204
        print(response.raw)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize(
    [  # values set
        'json_in', 'json_out'
    ],
    [  # answers set
        [  # 1st answer
            {  # 1st element [json_in] from 1st answer
                "name": "Jan",
                "surname": "Kowalski"
            },
            {
                "id": 1,
                "name": "Jan",
                "surname": "Kowalski",
                "register_date": "2021-04-01",
                "vaccination_date": "2021-04-09"
            }
        ]
    ]

)
def test_register_view(json_in, json_out):
    response = client.post(f"/register", json=json_in)
    dct_json = dict(response.json())
    assert response.status_code == 201
    assert dct_json['name'] == json_out['name']
    assert dct_json['surname'] == json_out['surname']
