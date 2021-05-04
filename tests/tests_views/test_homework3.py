import base64
from datetime import date

import pytest
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from views.main import app

client = TestClient(app)
client.counter = 0
login, passw = "4dm1n", "NotSoSecurePa$$"
token_hex = '773a7c51290f6448f44d25ae8bb330a6656940bce8fd54215ed3c270a67953bd'


def test_get_hello_html():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.text.find(f"<h1>Hello! Today date is {date.today()}</h1>") > 0
    assert bool(BeautifulSoup(response.text, 'html.parser').find())


@pytest.mark.parametrize(
    ['user', 'password', 'code', 'cookie'],
    [
        [login, passw, 201, token_hex],
        ["abc", "cde", 401, None]
    ]
)
def test_post_login_session(user, password, code, cookie):
    response = client.post("/login_session", auth=HTTPBasicAuth(user, password))
    coo = response.cookies.get("session_token")
    assert response.status_code == code
    assert coo == cookie


@pytest.mark.parametrize(
    ['response', 'code'],
    [
        [client.post("/login_token"), 401],
        [client.post("/login_token", auth=HTTPBasicAuth(login, passw)), 201]
    ]
)
def test_post_login_token(response, code):
    print(f"{response.status_code = }")
    print(f"{code = }")
    print(f"{response.json() = }")
    assert response.status_code == code
    # assert response.json() == {"token": token_hex}


# def test_get_welcome_session():
#     response = client.get('/welcome_session', cookies=dict())
#     coo1 = response.cookies.get('session_token')
#     assert not coo1
#     # assert response.status_code == 401
#     client.post("/login_token", auth=HTTPBasicAuth(login, passw))
#     response_get = client.get('/welcome_session',
#                               cookies=dict(session_token=token_hex))
#     coo2 = response_get.cookies.get('session_token')
#     assert response_get.status_code == 200
#     assert coo2 == token_hex


# @pytest.mark.parametrize(
#     ['code', 'post', 'get'],
#     [
#         [401, client.post("/login_token"), client.get('/welcome_session')],
#         [201,
#          client.post("/login_token", auth=HTTPBasicAuth(login, passw)),
#          client.get(f'/welcome_session?token={token_hex}')]
#     ]
# )
# def test_get_welcome_token(code, post, get):
#     assert get.status_code == code
#     # assert
