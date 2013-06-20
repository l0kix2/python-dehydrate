# coding: utf-8
"""
This module contains specs classes. Each of them knows about structures
which they can manipulate and how to fetch key and value for using in
dehydrating process.
This classes separated from Dehydrator class for ease of extending and adding
new spec types.
"""
from __future__ import unicode_literals

import six
from collections import Iterable, Mapping

from .helpers import Registry
from .exceptions import DehydrationException

registry = Registry()

# some handy shortcuts
is_string = lambda val: isinstance(val, six.string_types)
is_dict = lambda val: isinstance(val, Mapping)
is_iterable = lambda val: isinstance(val, Iterable)
is_two_tuple = lambda val: isinstance(val, tuple) and len(val) == 2


class Spec(object):

    _target_info = None
    _substitution = None

    def __init__(self, dehydrator, spec):
        self.dehydrator = dehydrator
        self.spec = spec

    @staticmethod
    def is_relevant(spec):
        """
        Field classes knows about specification of structures, which are
        relevant for them. So it can inform us whether this particular
        specification is acceptable by redefining this method.
        """
        raise NotImplementedError

    @property
    def target_info(self):
        if not self._target_info:
            self._target_info, self._substitution = self.parse_spec()
        return self._target_info

    @property
    def substitution(self):
        if not self._substitution:
            self._target_info, self._substitution = self.parse_spec()
        return self._substitution

    def parse_spec(self):
        """
        You should raise SpecParsingError if something goes wrong.
        """
        if is_two_tuple(self.spec):
            target_info, substitution = self.spec
        else:
            target_info = self.spec
            substitution = None

        try:
            self.validate_target_info(target_info)
        except Exception as e:
            raise DehydrationException(description=str(e))

        return target_info, substitution

    def validate_target_info(self, target_info):
        """
        Hook for validate target info, i. e. check keys or attributes if it is
        complex structure.
        """
        pass

    def build_key(self):
        return self.substitution or self.target

    def resolve_target(self, obj, target_name):
        # try to find getter method on dehydrator at first
        dehydrator_getter_name = self.dehydrator.GETTER_PREFIX + target_name
        if hasattr(self.dehydrator, dehydrator_getter_name):
            getter = getattr(self.dehydrator, dehydrator_getter_name)
            return getter(obj)

        if hasattr(obj, target_name):
            object_attribute = getattr(obj, target_name)
            if callable(object_attribute):
                return object_attribute()
            else:
                return object_attribute

        # TODO: more detailed exception
        raise DehydrationException("Can't resolve target %s" % target_name)


@registry.register
class SimpleSpec(Spec):

    @staticmethod
    def is_relevant(spec):
        if is_string(spec):
            return True
        if is_two_tuple(spec) and all(map(is_string, spec)):
            return True
        return False

    @property
    def target(self):
        return self.target_info

    def build_value(self, obj):
        return self.resolve_target(obj=obj, target_name=self.target)


@registry.register
class ComplexSpec(Spec):

    TARGET_FIELD_NAME = 'target'
    ITERABLE_FLAG_FIELD_NAME = 'iterable'
    DEHYDRATOR_FIELD_NAME = 'dehydrator'

    @staticmethod
    def is_relevant(spec):
        if is_dict(spec):
            return True
        if is_two_tuple(spec) and is_dict(spec[0]) and is_string(spec[1]):
            return True
        return False

    @classmethod
    def validate_target_info(cls, target_info):
        if not cls.TARGET_FIELD_NAME in target_info:
            message = (
                "'{field_name}' field is required in specification "
                "of {class_name}"
            )
            raise DehydrationException(description=message.format(
                field_name=cls.TARGET_FIELD_NAME,
                class_name=cls.__class__.__name__,
            ))

    def build_value(self, obj):
        target = self.resolve_target(obj=obj, target_name=self.target)

        dehydrator = self.dehydrator_cls(specs=self.specs)
        if self.is_iterable:
            return map(dehydrator.dehydrate, target)
        else:
            return dehydrator.dehydrate(target)

    @property
    def target(self):
        return self.target_info[self.TARGET_FIELD_NAME]

    @property
    def is_iterable(self):
        return self.target_info.get(self.ITERABLE_FLAG_FIELD_NAME, False)

    @property
    def dehydrator_cls(self):
        from dehydrate.base import Dehydrator
        return self.target_info.get(self.DEHYDRATOR_FIELD_NAME, Dehydrator)

    @property
    def specs(self):
        return self.target_info.get('specs')
