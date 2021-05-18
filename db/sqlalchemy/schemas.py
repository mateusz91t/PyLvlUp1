from typing import Optional

from pydantic import BaseModel, PositiveInt, constr


class ConfigSchema(BaseModel):
    class Config:
        orm_mode = True


class Shipper(ConfigSchema):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)


class SupplierIdName(ConfigSchema):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)


class SupplierAll(SupplierIdName):
    ContactName: Optional[constr(max_length=30)] = None
    ContactTitle: Optional[constr(max_length=30)] = None
    Address: Optional[constr(max_length=60)] = None
    City: Optional[constr(max_length=15)] = None
    Region: Optional[constr(max_length=15)] = None
    PostalCode: Optional[constr(max_length=10)] = None
    Country: Optional[constr(max_length=15)] = None
    Phone: Optional[constr(max_length=24)] = None
    Fax: Optional[constr(max_length=24)] = None
    HomePage: Optional[str] = None


class SupplierPost(ConfigSchema):
    CompanyName: constr(max_length=40)
    ContactName: Optional[constr(max_length=30)] = None
    ContactTitle: Optional[constr(max_length=30)] = None
    Address: Optional[constr(max_length=60)] = None
    City: Optional[constr(max_length=15)] = None
    PostalCode: Optional[constr(max_length=10)] = None
    Country: Optional[constr(max_length=15)] = None
    Phone: Optional[constr(max_length=24)] = None


class SupplierToAdd(SupplierPost):
    pass


class SupplierAdded(SupplierPost):
    SupplierID: PositiveInt
    Fax: Optional[constr(max_length=24)] = None
    HomePage: Optional[str] = None


class CategoryIdName(ConfigSchema):
    CategoryID: PositiveInt
    CategoryName: constr(max_length=40)


class Product(ConfigSchema):
    ProductID: PositiveInt
    ProductName: constr(max_length=40)
    Category: Optional[CategoryIdName]
    Discontinued: int
