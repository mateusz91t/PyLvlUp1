from fastapi.testclient import TestClient

from views.main import app

client = TestClient(app)


# async def setup_module():
#     await startup()
#
#
# async def teardown_module():
#     shutdown()


def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    # assert {"id": 1, "name": "Beverages"} in response.json()
