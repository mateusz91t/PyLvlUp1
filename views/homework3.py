from datetime import date

from fastapi import APIRouter, Request, Response, Cookie, HTTPException
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from myservices.auxiliary_methods import get_token_hex

homework3 = APIRouter()

templates = Jinja2Templates(directory='templates')

homework3.secret_key = "secret should be long because it is more secjurne"
login = '4dm1n'
password = 'NotSoSecurePa$$'
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
def post_login_session(response: Response, credentials: HTTPBasicCredentials):
    print(credentials)
    if credentials.username != login or credentials.password != password:
        response.status_code = 401
        raise HTTPException(status_code=401)
    else:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        response.set_cookie(key='session_token', value=token_hex)
        homework3.saved_session = token_hex
    return response

# @homework3.post("/login_session")
# def post_login_session(auth_header: Optional[str] = Header(None)):
#     print(auth_header)
#     # print(request.headers)
#     return dict(header=auth_header)


@homework3.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials):
    print(credentials)
    if credentials.username == login and credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        homework3.saved_token = token_hex
    else:
        response.status_code = 401
        raise HTTPException(status_code=401)
    return {"token": token_hex}
