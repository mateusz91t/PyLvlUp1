import pytest
from fastapi.testclient import TestClient

from db.sqlalchemy.crud import get_suppliers, get_supplier
from db.sqlalchemy.database import get_db
from views.main import app


@pytest.yield_fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_endpoint_get_suppliers(test_client):
    response = test_client.get("/suppliers")
    assert response.status_code == 200
    assert response.json()[0] == {"SupplierID": 1, "CompanyName": "Exotic Liquids"}
    assert response.json()[28] == {"SupplierID": 29, "CompanyName": "Forêts d'érables"}


def test_read_get_suppliers():
    suppliers = get_suppliers(next(get_db()))
    assert suppliers[0] == (1, 'Exotic Liquids')
    assert suppliers[28] == (29, "Forêts d'érables")


@pytest.mark.parametrize(
    ['supplier_id', 's_code', 'output'],
    [
        [24, 200, {
            "SupplierID": 24,
            "CompanyName": "G'day, Mate",
            "ContactName": "Wendy Mackenzie",
            "ContactTitle": "Sales Representative",
            "Address": "170 Prince Edward Parade Hunter's Hill",
            "City": "Sydney",
            "Region": "NSW",
            "PostalCode": "2042",
            "Country": "Australia",
            "Phone": "(02) 555-5914",
            "Fax": "(02) 555-4873",
            "HomePage": "G'day Mate (on the World Wide Web)#http://www.microsoft.com/accessdev/sampleapps/gdaymate.htm#"
        }],
        [2, 200, {
            "SupplierID": 2,
            "CompanyName": "New Orleans Cajun Delights",
            "ContactName": "Shelley Burke",
            "ContactTitle": "Order Administrator",
            "Address": "P.O. Box 78934",
            "City": "New Orleans",
            "Region": "LA",
            "PostalCode": "70117",
            "Country": "USA",
            "Phone": "(100) 555-4822",
            "Fax": None,
            "HomePage": "#CAJUN.HTM#"
        }],
        [-1, 422, {
            "detail": [
                {
                    "loc": [
                        "path",
                        "supplier_id"
                    ],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {
                        "limit_value": 0
                    }
                }
            ]
        }],
        [999, 404, {"detail": "Supplier not found"}]
    ]
)
def test_endpoint_get_supplier(test_client, supplier_id, s_code, output):
    response = test_client.get(f"/suppliers/{supplier_id}")
    assert response.status_code == s_code
    assert response.json() == output


def test_read_get_supplier():
    supplier = get_supplier(2, next(get_db()))
    assert supplier.SupplierID == 2
    assert supplier.CompanyName == "New Orleans Cajun Delights"
    assert supplier.ContactName == "Shelley Burke"
    assert supplier.ContactTitle == "Order Administrator"
    assert supplier.Address == "P.O. Box 78934"
    assert supplier.City == "New Orleans"
    assert supplier.Region == "LA"
    assert supplier.PostalCode == "70117"
    assert supplier.Country == "USA"
    assert supplier.Phone == "(100) 555-4822"
    assert supplier.Fax is None
    assert supplier.HomePage == "#CAJUN.HTM#"
