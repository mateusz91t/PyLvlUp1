import encodings
import hashlib


def count():
    i = 0
    while True:
        i += 1
        yield i


def get_hash(password: str):
    h = hashlib.sha512()
    h.update(bytes(password, encodings.normalize_encoding('utf8')))
    return h.hexdigest()
