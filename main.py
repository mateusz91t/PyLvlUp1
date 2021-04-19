from fastapi import FastAPI
from starlette.responses import JSONResponse

from myservices.classmodels import HelloNameResponse
from myservices.methods_for_main import count, get_hash

app = FastAPI()
app.counter = count()


# to run type:
# uvicorn main:app


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


@app.get("/auth")
def auth_view(password: str, password_hash: str):
    hashed = get_hash(password) == password_hash
    if hashed:
        response = JSONResponse()
        response.status_code = 204
        response.body = b''
        return response
    else:
        return JSONResponse(status_code=401)
