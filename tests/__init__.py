# coding: utf-8
from __future__ import unicode_literals


class Initer(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
