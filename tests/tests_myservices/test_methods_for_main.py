import pytest

from myservices.methods_for_main import get_hash, get_len


@pytest.mark.parametrize(
    ["password", "password_hash"],
    [
        ["haslo",
         "013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd"
         "62bbc27336153d0d316b2d13b36804080c44aa6198c533215"
         ],
        ["hasło",
         "25ca68b6012554ee6c6fa3ef73fe633c990ca165607ad937d7d8beb51da0b85ae2d228f06337ae2584a"
         "8aa80a890892c674da93a3e4475fe3bb0568c37d4b06d"
         ]
    ]
)
def test_check_password(password: str, password_hash: str):
    assert password_hash == get_hash(password)


@pytest.mark.parametrize(
    ['name', 'surname', 'sum_len'],
    [
        ['ąć ', '', 2],
        ['', 'aó-AóÓ', 5],
        ['!@#$%^&*()_+', '0123456789', 0]
    ]
)
def test_get_len(name: str, surname: str, sum_len: int):
    assert get_len(name, surname) == sum_len
