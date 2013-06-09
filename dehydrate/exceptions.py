# coding: utf-8
from __future__ import unicode_literals


class DehydrationException(Exception):
    pass
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)
    #
    # def __unicode__(self):
    #     if hasattr(self, 'msg'):
    #         return self.msg
    #     else:
    #         return ''


class SpecParsingError(DehydrationException):
    pass
