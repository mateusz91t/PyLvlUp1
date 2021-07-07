import re


# 2.1
def greetings(func):
    def inner(*args):
        return "Hello " + func(*args).title()

    return inner


# 2.2
def is_palindrome(function):
    def inner(*args):
        text = function(*args)
        trimmed_text = re.sub(r'(\W)', '', text)
        if trimmed_text.lower() == trimmed_text[::-1].lower():
            text += ' - is palindrome'
        else:
            text += ' - is not palindrome'
        return text

    return inner


# 2.3
def format_output(*args_output):
    def decorator(function):
        def inner(*args):
            source_json = function(*args)
            list_args_output = list(args_output)
            source_keys = list(source_json.keys())
            grouped_args = list()
            out_dict = dict()

            while list_args_output:
                arg = list_args_output.pop(0)
                if arg.__contains__('__'):
                    tmp_list = list()
                    splitted_args = arg.split('__')
                    for key in splitted_args:
                        tmp_list.append(key)
                    grouped_args.append(tmp_list)
                else:
                    grouped_args.append([arg])

            for vals in grouped_args:
                if set(vals) - set(source_keys):
                    raise ValueError('Choosen set of keys does not exists in source')

            while grouped_args:
                arg = grouped_args.pop(0)
                key = ''
                value = ''
                while arg:
                    element = arg.pop(0)
                    key += element + '__'
                    value += source_json[element] + ' '
                key = key.strip('__')
                value = value.strip()
                out_dict[key] = value

            return out_dict

        return inner

    return decorator


# 2.4
def add_class_method(cls):
    def decorator(function):
        setattr(cls, function.__name__, function)

        def inner(*args):
            return function(*args)

        return inner

    return decorator


def add_instance_method(cls):
    def decorator(function):
        def inner(self, *args):
            return function(*args)

        setattr(cls, function.__name__, inner)
        return function

    return decorator
