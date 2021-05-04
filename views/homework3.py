from datetime import date

from fastapi import APIRouter, Request, Response, Cookie, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.templating import Jinja2Templates

from myservices.auxiliary_methods import get_token_hex, get_response_by_format

homework3 = APIRouter()

templates = Jinja2Templates(directory='templates')

basic = HTTPBasic()

homework3.secret_key = "secret should be long because it is more secjurne"
login, password = '4dm1n', 'NotSoSecurePa$$'
homework3.saved_token = None
homework3.saved_session = None


# http://127.0.0.1:8000/hello
@homework3.get("/hello")
def get_hello_html(request: Request):
    return templates.TemplateResponse(
        "hello.html.j2",
        dict(request=request, tdate=str(date.today()))
    )


@homework3.post("/login_session", status_code=201)
def post_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(basic)):
    if credentials.username == login or credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        response.set_cookie(key='session_token', value=token_hex)
        homework3.saved_session = token_hex
    else:
        response.status_code = 401
        raise HTTPException(status_code=401)


@homework3.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials = Depends(basic)):
    if credentials.username == login and credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        homework3.saved_token = token_hex
    else:
        response.status_code = 401
        raise HTTPException(status_code=401)
    return {"token": token_hex}


@homework3.get('/welcome_session')
def get_welcome_session(response: Response, session_token: str = Cookie(None), format: str = ""):
    # print(session_token)
    # print(homework3.saved_session)
    if session_token != homework3.saved_session:
        raise HTTPException(status_code=401)
    return get_response_by_format(format)


@homework3.get('/welcome_token')
def get_welcome_session(response: Response, token: str, format: str = ""):
    if token != homework3.saved_token:
        raise HTTPException(status_code=401)
    return get_response_by_format(format)
