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
