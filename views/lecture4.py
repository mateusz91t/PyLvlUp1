import sqlite3

from fastapi import APIRouter, status

# It is possilble to use async lib aiosqlite alternatively
from myservices.classmodels import Customer

lecture4 = APIRouter()


@lecture4.on_event("startup")
async def startup():
    lecture4.db_connection = sqlite3.connect("db/northwind/northwind.db")  # from the absolute path of project ?
    lecture4.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # help for chinese chars


@lecture4.on_event("shutdown")
async def shutdown():
    lecture4.db_connection.close()


@lecture4.get("/products")
async def get_products():
    # I can run sql statement exactly at the connection, I don't need cursor
    products = lecture4.db_connection.execute("select * from products").fetchall()  # fetchall creates list of tuples
    output = dict(products_counter=len(products), products=products)  # list of tuples; 1 tuple == 1 row
    output2 = dict(
        products_counter=len(products),
        products=[row[1] for row in products]  # but U can take vals U need and create list of vals
    )
    return output


@lecture4.get("/products2")
async def get_products2():
    # Base on row factory U can change all result to your format, but it change the whole connection
    lecture4.db_connection.row_factory = lambda csr, row: row[1]
    # after that all rows will fetch with only one column value
    products = lecture4.db_connection.execute("select * from products").fetchall()  # fetchall creates list of tuples
    output = dict(products_counter=len(products), products=products)  # result changed by row factory
    return output


@lecture4.get("/products3")
async def get_products3():
    cursor = lecture4.db_connection.cursor()
    cursor.row_factory = lambda crs, row: row[1]  # row factory at the cursor like at the connection
    cursor.execute("select * from products")  # I don't have to execute and fetch in one line
    products = cursor.fetchall()
    return dict(products=products)


@lecture4.get("/suppliers/{supplier_id}")
async def get_supplier(supplier_id: int):
    cursor = lecture4.db_connection.cursor()
    cursor.row_factory = sqlite3.Row

    # format string is an dangerous method, vulnerable to SQL Injection
    # cursor.execute(f"select * from suppliers where supplierid = {supplier_id}")

    # better are placeholders ? with tuples, but not good if we have a lot of parameters
    # cursor.execute("select * from suppliers where supplierid = ?", (supplier_id,))

    # the longest but more safe and readable :name = {'name' = value}
    cursor.execute("select * from suppliers where supplierid = :supp_id", {'supp_id': supplier_id})

    # the problem is the out is not secured against null
    return dict(supplier=cursor.fetchone())


@lecture4.get("/emp_with_region")
async def get_emp_with_region():
    cursor = lecture4.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    emp_ter = cursor.execute("SELECT e.FirstName, e.LastName, t.TerritoryDescription "
                             "FROM Employees e INNER JOIN EmployeeTerritories et ON e.EmployeeID = et.EmployeeID "
                             "INNER JOIN Territories t on et.TerritoryID = t.TerritoryID").fetchall()
    return [
        dict(employee=f"{row['FirstName']} {row['LastName']}", region=row['TerritoryDescription'].rstrip())
        for row in emp_ter
    ]


@lecture4.get("/customers")
async def get_customers():
    cursor = lecture4.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    customers = cursor.execute("select * from customers").fetchall()
    return dict(customers=customers)


@lecture4.post("/customers/add", status_code=status.HTTP_201_CREATED)
async def post_customer(customer: Customer):
    cursor = lecture4.db_connection.cursor()
    cursor.execute(
        "INSERT INTO Customers"
        "(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) "
        "values "
        "(:c_id, :c_name, :contact_name, :contact_title, :addres, :city, :region, :postal_code, :country, :phone, :fax)",
        dict(c_id=customer.CustomerID,
             c_name=customer.CompanyName,
             contact_name=customer.ContactName,
             contact_title=customer.ContactTitle,
             addres=customer.Address,
             city=customer.City,
             region=customer.Region,
             postal_code=customer.PostalCode,
             country=customer.Country,
             phone=customer.Phone,
             fax=customer.Fax)
    )
    lecture4.db_connection.commit()

    # I can prepare an output, but I can return the whole instance of class, which will be serialized to json
    output = dict(CustomerID=customer.CustomerID,
                  CompanyName=customer.CompanyName,
                  ContactName=customer.ContactName,
                  ContactTitle=customer.ContactTitle,
                  Address=customer.Address,
                  City=customer.City,
                  Region=customer.Region,
                  PostalCode=customer.PostalCode,
                  Country=customer.Country,
                  Phone=customer.Phone,
                  Fax=customer.Fax)

    return customer


@lecture4.delete("/customers/delete/{customer_id}")
async def delete_customer(customer_id: str):
    cursor = lecture4.db_connection.execute("delete from customers where customerid = ?", [customer_id])
    lecture4.db_connection.commit()
    return dict(deleted=cursor.rowcount)
