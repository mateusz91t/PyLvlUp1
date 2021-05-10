import sqlite3

from fastapi import APIRouter, HTTPException

from myservices.classmodels import CategoryToAdd, CategoryAdded

homework4 = APIRouter()
emp_orders = {'last_name': 'LastName',
              'first_name': 'FirstName',
              'city': 'City',
              'EmployeeID': 'EmployeeID',
              '': "EmployeeID"}


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
        "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
        "COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || "
        "COALESCE(Country, '') full_address "
        "FROM Customers c ORDER BY UPPER(CustomerID);"
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


@homework4.get("/employees")
async def get_employees(limit: int = -1, offset: int = 0, order: str = ''):
    order = order.strip()
    if not (isinstance(limit, int) and isinstance(offset, int) and order in emp_orders.keys()):
        raise HTTPException(status_code=400)
    cursor = homework4.dbc.cursor()
    cursor.row_factory = sqlite3.Row
    employees = cursor.execute(
        "SELECT EmployeeID id, LastName last_name, FirstName first_name, City city "
        f"FROM Employees ORDER BY {emp_orders[order]} LIMIT :lim OFFSET :off;"
        , {"lim": limit, "off": offset}
    ).fetchall()
    return dict(employees=employees)


@homework4.get("/products_extended")
async def get_products_extended():
    cursor = homework4.dbc.cursor()
    cursor.row_factory = sqlite3.Row
    products = cursor.execute(
        "SELECT p.ProductID id, p.ProductName name, c.CategoryName category, s.CompanyName supplier "
        "FROM Products p LEFT JOIN Categories c on p.CategoryID = c.CategoryID "
        "LEFT JOIN Suppliers s on p.SupplierID = s.SupplierID ORDER BY p.ProductID;"
    ).fetchall()
    return dict(products_extended=products)


@homework4.get("/products/{id}/orders")
async def get_orders_by_id_product(id: int):
    cursor = homework4.dbc.cursor()
    cursor.row_factory = sqlite3.Row
    product = cursor.execute(
        "SELECT p.ProductID FROM Products p where p.ProductID = ?", (id,)
    ).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Id not found")
    orders = cursor.execute(
        "SELECT o.OrderID id, c.CompanyName customer, od.Quantity quantity, "
        "ROUND((od.UnitPrice * od.Quantity) - (od.Discount * od.UnitPrice * od.Quantity), 2) total_price "
        "FROM Orders o INNER JOIN 'Order Details' od on o.OrderID = od.OrderID "
        "INNER JOIN Products p on od.ProductID = p.ProductID LEFT JOIN Customers c on o.CustomerID = c.CustomerID "
        "WHERE p.ProductID = ? ORDER BY o.OrderID"
        , (id,)
    ).fetchall()
    return dict(orders=orders)


@homework4.post("/categories", status_code=201, response_model=CategoryAdded)
async def post_category(category: CategoryToAdd):
    cursor = homework4.dbc.cursor()
    cursor.execute("INSERT INTO Categories (CategoryName) VALUES (?);", (category.name,))
    category_added = CategoryAdded(name=category.name, id=cursor.lastrowid)
    homework4.dbc.commit()
    return category_added


@homework4.put("/categories/{id}", response_model=CategoryAdded)
async def put_category(id: int, category: CategoryToAdd):
    cursor = homework4.dbc.cursor()
    cursor.execute("UPDATE Categories SET CategoryName = :cname WHERE CategoryID = :cid;"
                   , dict(cname=category.name, cid=id))
    print(f"{cursor.lastrowid = }")  # why cursor.lastrowid return 0??
    if cursor.rowcount <= 0:
        raise HTTPException(status_code=404, detail="Id not found")
    category_added = CategoryAdded(name=category.name, id=id)  # why cursor.lastrowid return 0??
    homework4.dbc.commit()
    return category_added


@homework4.delete("/categories/{id}")
async def delete_category(id: int):
    cursor = homework4.dbc.cursor()
    cursor.execute("DELETE FROM Categories WHERE CategoryID = ?;", (id,))
    if cursor.rowcount <= 0:
        raise HTTPException(status_code=404, detail="Id not found")
    homework4.dbc.commit()
    return dict(deleted=cursor.rowcount)
