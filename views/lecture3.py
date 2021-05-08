from hashlib import sha256
from typing import List

from fastapi import Request, Query, APIRouter, Response, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

lecture2 = APIRouter()

templates = Jinja2Templates(directory='templates')

lecture2.secret_key = "secret should be long because it is more secjurne"
lecture2.access_tokens = list()


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


# http://127.0.0.1:8000/lec2/sample_path/1123
@lecture2.get("/sample_path/{sample_value}")
def get_sample_path_json(sample_value: int):
    print(f"{sample_value = }")
    print(type(sample_value))
    return {'sample_value': sample_value}


# http://127.0.0.1:8000/lec2/fip/adssdasd%20%20/%20/%20/%20/%20213%201
@lecture2.get("/fip/{file_path:path}")
def get_file_path(file_path: str):
    return dict(file_path=file_path)


# http://127.0.0.1:8000/lec2/login?user=abc&password=bcd
@lecture2.get("/login")
def get_login(user: str, password: str, response: Response):
    session_token = sha256(f"{user}:{password}{lecture2.secret_key}".encode()).hexdigest()
    lecture2.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    print(f"{session_token = }")
    return dict(message='Welcome')


# curl -X 'GET' 'http://127.0.0.1:8000/lec2/data' -H 'accept: application/json' -H 'Cookie: session_token=d9cb503f61d7b77ede3821ecc11c28524d90807444085b466ca8dc9df59e992b'
@lecture2.get("/data")
def get_secured_data(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in lecture2.access_tokens:
        raise HTTPException(status_code=403, detail='Unauthorized')
    else:
        return dict(message="Secure Content")
