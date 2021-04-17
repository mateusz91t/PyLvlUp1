from fastapi import FastAPI
from pydantic import BaseModel

from myserives.methods_for_main import count

app = FastAPI()
app.counter = count()


# to run type:
# uvicorn main:app

class HelloNameResponse(BaseModel):
    message: str


@app.get('/')
def root_view():
    return {'message': "Hello"}


@app.get("/hello/{name}", response_model=HelloNameResponse)
def hello_name_view(name: str):
    return HelloNameResponse(message=f"Hello {name}")


@app.get("/counter")
def counter_viev():
    return next(app.counter)


@app.options("/method")
def method_view():
    return {"method": "options"}
