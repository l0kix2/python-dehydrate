# coding: utf-8
from __future__ import unicode_literals

from .helpers import wrap_in_dict
from . import specs


class Dehydrator(object):

    GETTER_PREFIX = 'get_'

    specs = None

    def __init__(self, specs=None):
        self.specs = specs or self.specs or ()

    @wrap_in_dict
    def dehydrate(self, obj):
        for spec in self.specs:
            yield self.dehydrate_spec(obj, spec)

    def dehydrate_spec(self, obj, spec):
        spec = self.wrap_spec(spec)
        return spec.build_key(), spec.build_value(obj)

    def wrap_spec(self, spec):
        for spec_cls in specs.registry:
            if spec_cls.is_relevant(spec):
                return spec_cls(dehydrator=self, spec=spec)
