from datetime import datetime as dt, timedelta
from typing import Optional

from fastapi import FastAPI, Response
from starlette.responses import JSONResponse

from myservices.classmodels import HelloNameResponse, PatientResponse, ToRegisterResponse
from myservices.methods_for_main import count, get_hash, get_len

app = FastAPI()
app.counter = count()
app.register_counter = count()
app.patient = dict()


# to run type:
# uvicorn main:app


@app.get('/')
def root_view():
    return {'message': 'Hello world!'}


@app.get("/hello/{name}", response_model=HelloNameResponse)
def hello_name_view(name: str):
    return HelloNameResponse(message=f"Hello {name}")


@app.get("/counter")
def counter_viev():
    return next(app.counter)


@app.options("/method")
def method_view():
    return {"method": "OPTIONS"}


@app.get("/method")
def method_view():
    return {"method": "GET"}


@app.delete("/method")
def method_view():
    return {"method": "DELETE"}


@app.put("/method")
def method_view():
    return {"method": "PUT"}


@app.post("/method", status_code=201)
def method_view():
    return {"method": "POST"}


@app.get("/auth")
def auth_view(password: str = '', password_hash: str = ''):
    hashed = get_hash(password) == password_hash
    print(password)
    print(password_hash)
    if hashed and password and password_hash:
        status_code = 204
    else:
        status_code = 401
    return Response(status_code=status_code)


@app.post("/register", status_code=201, response_model=PatientResponse)
def register_view(request: ToRegisterResponse):
    key = next(app.register_counter)
    name = request.name
    surname = request.surname
    r_date = dt.date(dt.now())
    v_date = r_date + timedelta(get_len(name, surname))
    request_out = PatientResponse(
        id=key,
        name=name,
        surname=surname,
        register_date=str(r_date),
        vaccination_date=str(v_date)
    )
    app.patient[key] = dict(request_out)
    return request_out


@app.get("/patient/{id}")
def patient_view(id: int):
    id_int = int(id)
    if id_int < 0:
        return JSONResponse(status_code=400, content="id cannot be lower than 0")
    elif id_int in app.patient:
        patient = app.patient[id_int]
        response = PatientResponse(
            id=id_int,
            name=patient['name'],
            surname=patient['surname'],
            register_date=patient['register_date'],
            vaccination_date=patient['vaccination_date']
        )
        return response
    else:
        return JSONResponse(status_code=404, content="not found your patient id")
