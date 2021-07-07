import pytest

from hw2 import greetings, is_palindrome, format_output, add_class_method, add_instance_method


def test_greetings():
    @greetings
    def name_surname():
        return "jan nowak"

    @greetings
    def n1(text):
        return f' ${text}$'

    assert name_surname() == "Hello Jan Nowak"
    assert n1('Ala') == "Hello  $Ala$"


def test_is_palindrome():
    @is_palindrome
    def sentence():
        return "Łapał za kran, a kanarka złapał."

    @is_palindrome
    def sentence2(t):
        return "Łapał za kran, a kanarka złapał." + t

    assert sentence() == "Łapał za kran, a kanarka złapał. - is palindrome"
    assert sentence2('') == "Łapał za kran, a kanarka złapał. - is palindrome"
    assert sentence2('asd') != "Łapał za kran, a kanarka złapał. - is not palindrome"


def test_format_output():
    @format_output("first_name__last_name", "city")
    def first_func():
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": "Warsaw"
        }

    @format_output("first_name", "age")
    def second_func():
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": "Warsaw"
        }

    assert first_func() == {"first_name__last_name": "Jan Kowalski", "city": "Warsaw"}

    with pytest.raises(ValueError):
        second_func()


def test_class_method():
    class A:
        pass

    @add_class_method(A)
    def foo():
        return "Hello!"

    @add_instance_method(A)
    def bar():
        return "Hello again!"

    assert A.foo() == "Hello!"
    assert A().bar() == "Hello again!"
