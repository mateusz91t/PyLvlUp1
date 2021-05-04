from datetime import date

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

homework3 = APIRouter()

templates = Jinja2Templates(directory='templates')


# http://127.0.0.1:8000/hello
@homework3.get("/hello")
def get_hello_html(request: Request):
    return templates.TemplateResponse(
        "hello.html.j2",
        dict(request=request, tdate=str(date.today()))
    )
