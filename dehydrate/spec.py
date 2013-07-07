# coding: utf-8
from __future__ import unicode_literals


class Spec(object):
    # TODO: maybe decorator
    def __init__(self, target, substitution=None, type='simple', **kwargs):
        self.target = target
        self.substitution = substitution
        self.type = type

        for key, value in kwargs.items():
            setattr(self, key, value)

    # TODO: immutable


# handy shortcut
S = Spec
