import sqlite3

from fastapi import APIRouter, HTTPException

homework4 = APIRouter()


@homework4.on_event("startup")
async def startup():
    homework4.dbc = sqlite3.connect("db/northwind/northwind.db")
    homework4.dbc.text_factory = lambda b: b.decode(errors='ignore')


@homework4.on_event("shutdown")
async def shutdown():
    homework4.dbc.close()


@homework4.get("/categories")
async def get_categories():
    cursor = homework4.dbc.cursor()
    categories = cursor.execute("SELECT  CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    output = dict(categories=[dict(id=row[0], name=row[1]) for row in categories])
    return output


@homework4.get("/customers")
async def get_customers():
    cursor = homework4.dbc.cursor()
    cursor.row_factory = sqlite3.Row
    customers = cursor.execute(
        "SELECT rtrim(CustomerID) id, "
        "rtrim(COALESCE(CompanyName, '')) name, "
        "CASE "
        "   TRIM(rtrim(COALESCE(Address, '')) || ' ' || rtrim(COALESCE(PostalCode, '')) || ' ' || "
        "   rtrim(COALESCE(City, '')) || ' ' || rtrim(COALESCE(Country, ''))) "
        "   WHEN  '' THEN NULL "
        "   ELSE rtrim(COALESCE(Address, '')) || ' ' || rtrim(COALESCE(PostalCode, '')) || ' ' || "
        "   rtrim(COALESCE(City, '')) || ' ' || rtrim(COALESCE(Country, '')) "
        "END full_address FROM Customers c ORDER BY UPPER(CustomerID);"
    ).fetchall()
    return dict(customers=customers)


@homework4.get("/products/{id}")
async def get_product(id: int):
    if not isinstance(id, int):
        raise HTTPException(status_code=404, detail="Id not found")
    cursor = homework4.dbc.cursor()
    cursor.row_factory = sqlite3.Row
    product = cursor.execute(
        "SELECT ProductID id, RTRIM(ProductName) name FROM Products p WHERE ProductID = ?",
        (id,)
    ).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Id not found")
    return product
