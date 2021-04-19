from datetime import datetime as dt, timedelta

from fastapi import FastAPI
from starlette.responses import JSONResponse

from myservices.classmodels import HelloNameResponse, RegisteredResponse, ToRegisterResponse
from myservices.methods_for_main import count, get_hash

app = FastAPI()
app.counter = count()
app.register_counter = count()


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


app.post("/register")


@app.post("/register", status_code=201, response_model=RegisteredResponse)
def register_view(request: ToRegisterResponse):
    name = request.name
    surname = request.surname
    r_date = dt.date(dt.now())
    v_date = r_date + timedelta(len(name) + len(surname))
    request_out = RegisteredResponse(
        id=next(app.register_counter),
        name=request.name,
        surname=request.surname,
        register_date=str(r_date),
        vaccination_date=str(v_date)
    )
    return request_out
