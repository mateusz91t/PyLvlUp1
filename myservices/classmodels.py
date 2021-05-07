from pydantic import BaseModel


class HelloNameResponse(BaseModel):
    message: str


class PatientResponse(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


class ToRegisterResponse(BaseModel):
    name: str
    surname: str


class Customer(BaseModel):
    CustomerID: str
    CompanyName: str
    ContactName: str
    ContactTitle: str
    Address: str
    City: str
    Region: str
    PostalCode: str
    Country: str
    Phone: str
    Fax: str
