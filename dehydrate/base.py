# coding: utf-8
from __future__ import unicode_literals

from .exceptions import UnknownSpecFormat, HandlerNotFound
from .helpers import is_string, is_two_str_tuple
from .spec import S
from . import handlers


class Dehydrator(object):

    GETTER_PREFIX = 'get_'

    specs = None

    def __init__(self, specs=None):
        self.specs = specs or self.specs or ()

    def dehydrate(self, obj):
        if obj is None:
            return None

        return dict(
            self.dehydrate_spec(obj, spec)
            for spec in self.specs
        )

    def dehydrate_spec(self, obj, spec):
        spec = self.wrap_spec_if_needed(spec)
        handler = self.select_handler(spec)
        return handler.build_key(), handler.build_value(obj)

    def wrap_spec_if_needed(self, spec):
        if is_string(spec):
            return S(spec)
        elif is_two_str_tuple(spec):
            return S(*spec)
        elif isinstance(spec, S):
            return spec
        else:
            raise UnknownSpecFormat(spec=spec)

    def select_handler(self, spec):
        spec_type = spec.type
        if not spec_type in handlers.registry:
            raise HandlerNotFound(spec_type=spec_type)
        handler_cls = handlers.registry[spec_type]
        return handler_cls(spec=spec, dehydrator=self)
