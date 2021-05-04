from datetime import datetime as dt, timedelta

from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_mako import FastAPIMako

from myservices.classmodels import HelloNameResponse, PatientResponse, ToRegisterResponse
from myservices.methods_for_main import count, get_hash, get_len
from views.homework3 import homework3
from views.lecture3 import lecture2

app = FastAPI()

app.counter = count()
app.register_counter = count()
app.patient = dict()

app.include_router(
    lecture2,
    prefix="/lec2",
    tags=["lecture2"]
)

app.__name__ = 'templates'
mako = FastAPIMako(app)

app.include_router(
    homework3,
    tags=["homework2"]
)

# to run type:
# uvicorn main:app
# uvicorn views.main:app --reload


@app.get('/')
def root_view():
    return {'message': 'Hello world!'}


@app.get("/hello/{name}", response_model=HelloNameResponse)
def hello_name_view(name: str):
    return HelloNameResponse(message=f"Hello {name}")


@app.get("/counter")
def counter_viev():
    return next(app.counter)


@app.post("/method", status_code=201)
@app.api_route(path="/method", methods=["OPTIONS", "GET", "DELETE", "PUT"], )
def method_view(request: Request):
    return {"method": request.method}


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


# how to move up this to other file?
# http://127.0.0.1:8000/lec2/mako
@app.get("/mako", response_class=HTMLResponse)
@mako.template('index.html.mako')
def get_mako_html(request: Request):
    setattr(request, 'mako', 'test')
    return {"my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]}
