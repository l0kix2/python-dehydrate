# coding: utf-8
from __future__ import unicode_literals

from .base import Dehydrator


def dehydrate(obj, cls=Dehydrator, fields=None):
    return cls(fields=fields).dehydrate(obj)
