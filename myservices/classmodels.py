from pydantic import BaseModel


class HelloNameResponse(BaseModel):
    message: str


class RegisteredResponse(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


class ToRegisterResponse(BaseModel):
    name: str
    surname: str
