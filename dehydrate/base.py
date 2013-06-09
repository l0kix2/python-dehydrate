# coding: utf-8
from __future__ import unicode_literals

from .helpers import wrap_in_dict
from . import fields


class Dehydrator(object):

    GETTER_PREFIX = 'get_'

    fields = None

    def __init__(self, fields=None):
        self.fields = fields or self.fields or ()

    @wrap_in_dict
    def dehydrate(self, obj):
        for spec in self.fields:
            yield self.dehydrate_field(obj, spec)

    def dehydrate_field(self, obj, spec):
        field = self.wrap_field(spec)
        return field.build_key(), field.build_value(obj)

    def wrap_field(self, spec):
        for field_cls in fields.registry:
            if field_cls.is_relevant(spec):
                return field_cls(dehydrator=self, spec=spec)
