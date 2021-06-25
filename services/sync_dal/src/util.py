import functools


class WebExeception(Exception):
    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)

    def __str__(self):
        return str(self.msg)


def exc_handler(func):
    @functools.wraps(func)
    def inner_f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WebExeception as e:
            return {'error': e.msg}, e.status_code
    return inner_f
