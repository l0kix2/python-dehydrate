# coding: utf-8
from __future__ import unicode_literals

from functools import wraps


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


class Registry(object):
    def __init__(self):
        self._registry = set()

    def _register(self, item):
        self._registry.add(item)

    def register(self, obj):
        self._register(obj)
        return obj

    def __iter__(self):
        return self._registry.__iter__()
