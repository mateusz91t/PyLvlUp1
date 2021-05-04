import encodings
import hashlib
import re
from fastapi.responses import HTMLResponse, PlainTextResponse


def count():
    i = 0
    while True:
        i += 1
        yield i


def get_hash(password: str):
    h = hashlib.sha512()
    h.update(bytes(password, encodings.normalize_encoding('utf8')))
    return h.hexdigest()


def get_len(name: str, surname: str):
    pattern = re.compile(r'([A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż])')
    name_letters = pattern.findall(name)
    surname_letters = pattern.findall(surname)
    return len(name_letters) + len(surname_letters)


def get_token_hex(login: str, password: str, secret_key: str) -> str:
    token_str = f"{login}:{password}|{secret_key}"
    token_encoded = token_str.encode()
    token_hex = hashlib.sha256(token_encoded).hexdigest()
    return token_hex


def get_response_by_format(format: str = '', message: str = 'Welcome!'):
    if format == 'json':
        return {"message": f"{message}"}
    elif format == 'html':
        return HTMLResponse(content=f"<h1>{message}</h1>")
    else:
        return PlainTextResponse(content=f"{message}")
