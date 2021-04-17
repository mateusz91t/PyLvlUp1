from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    print(response)
    print(response.text)
    print(response.raw)
    print(response.reason)
    print(response.content)

# pytest -v -W ignore::DeprecationWarning
# -v wyświetli szczegółowe inf o testach
# -W pozwoli ukryć warningi wymienionego typu
