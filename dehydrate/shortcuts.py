# coding: utf-8
from __future__ import unicode_literals

from .base import Dehydrator


def dehydrate(obj, cls=Dehydrator, specs=None, empty=None):
    return cls(specs=specs, empty=empty).dehydrate(obj=obj)
