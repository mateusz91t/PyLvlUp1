from datetime import datetime as dt, timedelta
from typing import List

from fastapi import FastAPI, Response, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_mako import FastAPIMako

from myservices.classmodels import HelloNameResponse, PatientResponse, ToRegisterResponse
from myservices.methods_for_main import count, get_hash, get_len
from views.main import mako, app

lecture2 = APIRouter()

templates = Jinja2Templates(directory='templates')


# http://127.0.0.1:8000/lec2/request_query_string_discovery/?asd=2&aac=abc
@lecture2.get("/request_query_string_discovery/")
def get_all_query_params(request: Request):
    qp = request.query_params
    print(f"{qp = }")
    return qp


# http://127.0.0.1:8000/lec2/request_query_string_discovery2/?u=1&q=2&u=3&q=4
@lecture2.get("/request_query_string_discovery2/")
def get_all_query_params2(u: str = Query("default"), q: List[int] = Query(None)):
    query_items = {"q": q, "u": u}
    return query_items


# http://127.0.0.1:8000/lec2/static
@lecture2.get("/static", response_class=HTMLResponse)
def get_static():
    return """
    <html>
        <head>
            <title>Statyczna stronka</title>
        </head>
        <body>
            <h1>Look at me! HTML!!</h1>
        </body>
    </html>"""


# http://127.0.0.1:8000/lec2/jinja2
@lecture2.get("/jinja2")
def get_jinja_html(request: Request):
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]})


# 127.0.0.1:8000/lec2/sample_path/1123
@lecture2.get("/sample_path/{sample_value}")
def get_sample_path_json(sample_value: int):
    print(f"{sample_value = }")
    print(type(sample_value))
    return {'sample_value': sample_value}


# http://127.0.0.1:8000/lec2/fip/adssdasd%20%20/%20/%20/%20/%20213%201
@lecture2.get("/fip/{file_path:path}")
def get_file_path(file_path: str):
    return dict(file_path=file_path)
