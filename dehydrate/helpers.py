# coding: utf-8
from __future__ import unicode_literals

from functools import wraps
import six


# TODO: move this decorator in some common lib and set it in depends.
def wrap_in_dict(func):
    """
    Takes callable, which yields or returns key-value pairs and makes dict of
    them. Helps in making function shorter and simpler.
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        return dict(func(*args, **kwargs))
    return decorator


is_string = lambda obj: isinstance(obj, six.string_types)
is_two_tuple = lambda obj: isinstance(obj, tuple) and len(obj) == 2
is_two_str_tuple = lambda obj: is_two_tuple(obj) and all(map(is_string, obj))


class Registry(dict):
    def register(self, key):
        def decorator(obj):
            self[key] = obj
            return obj
        return decorator
