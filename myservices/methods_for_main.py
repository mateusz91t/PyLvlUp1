import encodings
import hashlib
import re


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
