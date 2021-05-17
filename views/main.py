from datetime import datetime as dt, timedelta

from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse
import fastapi_mako

from myservices.classmodels import HelloNameResponse, PatientResponse, ToRegisterResponse
from myservices.auxiliary_methods import count, get_hash, get_len
from views.homework3 import homework3
from views.homework4 import homework4
from views.lecture3 import lecture2
from views.lecture4 import lecture4
from views.lecture5 import lecture5

app = FastAPI()

app.counter = count()
app.register_counter = count()
app.patient = dict()

app.include_router(lecture2, tags=["lecture2"])

app.__name__ = 'templates'
mako = fastapi_mako.FastAPIMako(app)

app.include_router(homework3, tags=["homework2"])
app.include_router(lecture4, prefix="/lec4", tags=["lecture4"])
app.include_router(homework4, tags=["homework4"])
app.include_router(lecture5, prefix="/lec5", tags=["lecture5"])


# to run type:
# docker-compose up
# uvicorn views.main:app --reload
# run with postgres [Linux]:
# SQLALCHEMY_DATABASE_URL="postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres" uvicorn views.main:app --reload --host=0.0.0.0 --port=${PORT:-5000}
# or to set the env variable in Win10 with venv (e.g. PyCharm)
# set SQLALCHEMY_DATABASE_URL=postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres
# and next you can run with: uvicorn views.main:app

# connecting to DB locally:
# 1) run a docker
# 2) docker-compose up
# 3) docker-compose exec postgres bash
# 3) psql -U postgres
# 5) select * ....
# 6) to see tables: \dt  to exit: \q

# DB migration:
# 1) connect to docker
# 2) psql -U postgres < docker-entrypoint-initdb.d/migration.sql

# send a dump to heroku [RAW FILE !!! not preview]:
# heroku pg:backups:restore https://github.com/mateusz91t/PyLvlUp1/raw/master/migrations/northwind.dump --app py-lvl-up-1 --confirm py-lvl-up-1


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
