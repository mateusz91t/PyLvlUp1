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
homework3.saved_cookies = list()


# http://127.0.0.1:8000/hello
@homework3.get("/hello")
def get_hello_html(request: Request):
    return templates.TemplateResponse(
        "hello.html.j2",
        dict(request=request, tdate=str(date.today()))
    )


@homework3.post("/login_session", status_code=201)
def post_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(basic)):
    if credentials.username == login and credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        response.set_cookie(key='session_token', value=token_hex)
        if len(homework3.saved_cookies) >= 3:
            del homework3.saved_cookies[0]
        homework3.saved_cookies.append(token_hex)
    else:
        raise HTTPException(status_code=401)
    print(homework3.saved_cookies)


@homework3.post("/login_token", status_code=201)
def post_login_token(credentials: HTTPBasicCredentials = Depends(basic)):
    if credentials.username == login and credentials.password == password:
        token_hex = get_token_hex(credentials.username, credentials.password, homework3.secret_key)
        if len(homework3.saved_tokens) >= 3:
            del homework3.saved_tokens[0]
        homework3.saved_tokens.append(token_hex)
    else:
        raise HTTPException(status_code=401)
    print(homework3.saved_tokens)
    return {"token": token_hex}


@homework3.get('/welcome_session')
def get_welcome_session(session_token: str = Cookie(None), format: str = ""):
    print(homework3.saved_cookies)
    if session_token not in homework3.saved_cookies:
        raise HTTPException(status_code=401)
    return get_response_by_format(format)


@homework3.get('/welcome_token')
def get_welcome_session(token: str, format: str = ""):
    print(homework3.saved_tokens)
    if token not in homework3.saved_tokens:
        raise HTTPException(status_code=401)
    return get_response_by_format(format)


@homework3.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: str = ""):
    print(homework3.saved_cookies)
    if session_token not in homework3.saved_cookies:
        raise HTTPException(status_code=401)
    homework3.saved_cookies = list(filter(lambda x: x != session_token, homework3.saved_cookies))
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=303)


@homework3.delete("/logout_token")
def logout_token(token: str = "", format: str = ""):
    print(homework3.saved_tokens)
    if token not in homework3.saved_tokens:
        raise HTTPException(status_code=401)
    homework3.saved_tokens = list(filter(lambda x: x != token, homework3.saved_tokens))
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=303)


@homework3.get("/logged_out")
def logged_out(format: str = ""):
    return get_response_by_format(format, 'Logged out!')
