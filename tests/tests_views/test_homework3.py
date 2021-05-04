from datetime import date
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from views.main import app

client = TestClient(app)
client.counter = 0


def test_get_hello_html():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.text.find(f"<h1>Hello! Today date is {date.today()}</h1>") > 0
    assert bool(BeautifulSoup(response.text, 'html.parser').find())
