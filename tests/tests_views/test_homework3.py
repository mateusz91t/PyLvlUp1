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
str_log_ps = f"{login}:{passw}"
b64_str = base64.b64encode(str_log_ps.encode(encoding='utf-8'))
token_value = "xyz"  # todo change token to sha256
token_hex = '773a7c51290f6448f44d25ae8bb330a6656940bce8fd54215ed3c270a67953bd'


def test_get_hello_html():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.text.find(f"<h1>Hello! Today date is {date.today()}</h1>") > 0
    assert bool(BeautifulSoup(response.text, 'html.parser').find())


def x_test_post_login_session():
    response = client.post(
        "/login_session",
        headers={"Authorization": f"Basic {b64_str}"}
    )
    cookie = response.cookies.get("session_token")
    assert response.status_code == 201
    assert bool(cookie)


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
