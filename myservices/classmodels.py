from pydantic import BaseModel


class HelloNameResponse(BaseModel):
    message: str
