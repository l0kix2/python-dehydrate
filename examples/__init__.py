# coding: utf-8
from __future__ import unicode_literals


class Person(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
