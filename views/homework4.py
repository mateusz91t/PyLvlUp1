import sqlite3

from fastapi import APIRouter

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
    customers = cursor.execute("SELECT rtrim(CustomerID) id, "
                                "rtrim(CompanyName) name, "
                                "rtrim(Address || ' ' || PostalCode || ' ' || City || ' ' || Country) full_address "
                                "FROM Customers c ORDER BY CustomerID").fetchall()
    return dict(categories=customers)
