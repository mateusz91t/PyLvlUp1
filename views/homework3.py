from datetime import date

from fastapi import APIRouter, Request, Response, Cookie, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.templating import Jinja2Templates

from myservices.auxiliary_methods import get_token_hex, get_response_by_format

homework3 = APIRouter()

templates = Jinja2Templates(directory='templates')

basic = HTTPBasic()

homework3.secret_key = "secret should be long because it is more secjurne"
login, password = '4dm1n', 'NotSoSecurePa$$'
homework3.saved_tokens = list()
homework3.saved_sessions = list()


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
        if len(homework3.saved_sessions) > 3:
            del homework3.saved_sessions[0]
        homework3.saved_sessions.append(token_hex)
    else:
        response.status_code = 401
        raise HTTPException(status_code=401)
    print(homework3.saved_sessions)


@homework3.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials = Depends(basic)):
    if credentials.username == login and credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        if len(homework3.saved_tokens) > 3:
            del homework3.saved_tokens[0]
        homework3.saved_tokens.append(token_hex)
    else:
        response.status_code = 401
        raise HTTPException(status_code=401)
    print(homework3.saved_tokens)
    return {"token": token_hex}


@homework3.get('/welcome_session')
def get_welcome_session(response: Response, session_token: str = Cookie(None), format: str = ""):
    if session_token not in homework3.saved_sessions:
        raise HTTPException(status_code=401)
    print(homework3.saved_sessions)
    return get_response_by_format(format)


@homework3.get('/welcome_token')
def get_welcome_session(response: Response, token: str, format: str = ""):
    if token not in homework3.saved_tokens:
        raise HTTPException(status_code=401)
    print(homework3.saved_tokens)
    return get_response_by_format(format)


@homework3.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: str = ""):
    if session_token not in homework3.saved_sessions:
        raise HTTPException(status_code=401)
    homework3.saved_sessions.remove(session_token)
    print(homework3.saved_sessions)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@homework3.delete("/logout_token")
def logout_token(session_token: str, format: str = ""):
    if session_token not in homework3.saved_tokens:
        raise HTTPException(status_code=401)
    homework3.saved_tokens.remove(session_token)
    print(homework3.saved_tokens)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@homework3.delete("/logged_out", status_code=200)
@homework3.get("/logged_out")
def logged_out(format: str = ""):
    return get_response_by_format(format, 'Logged out!')
