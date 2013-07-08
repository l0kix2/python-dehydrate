# coding: utf-8
"""
This module contains handlers for different spec types.
This classes separated from Dehydrator class for ease of extending and adding
new spec types.
"""
from __future__ import unicode_literals

from .exceptions import TargetResolvingError
from .helpers import Registry

registry = Registry()


class Handler(object):

    def __init__(self, spec, dehydrator):
        self.spec = spec
        self.dehydrator = dehydrator

    def build_key(self):
        return self.spec.substitution or self.spec.target

    @property
    def target(self):
        return self.spec.target

    def resolve_target(self, obj, target):
        # try to find getter method on dehydrator at first
        dehydrator_getter_name = self.dehydrator.GETTER_PREFIX + target
        if hasattr(self.dehydrator, dehydrator_getter_name):
            getter = getattr(self.dehydrator, dehydrator_getter_name)
            return getter(obj)

        if hasattr(obj, target):
            object_attribute = getattr(obj, target)
            if callable(object_attribute):
                return object_attribute()
            else:
                return object_attribute

        raise TargetResolvingError(
            target=target,
            dehydrator=self.dehydrator,
            obj=obj,
        )


@registry.register('simple')
class SimpleHandler(Handler):

    def build_value(self, obj):
        value = self.resolve_target(obj=obj, target=self.target)

        post_hook_name = 'post_handle_value'
        if hasattr(self.dehydrator, post_hook_name):
            value = getattr(self.dehydrator, post_hook_name)(value)

        return value


@registry.register('nested')
class NestedHandler(Handler):

    def build_value(self, obj):
        if obj is None:
            # Think about customizing ability in this place.
            return None

        target = self.resolve_target(obj=obj, target=self.target)

        dehydrator = self.dehydrator_cls(specs=self.specs)

        return self.apply_dehydrator(dehydrator, target)

    def apply_dehydrator(self, dehydrator, target):
        return dehydrator.dehydrate(target)

    @property
    def dehydrator_cls(self):
        from dehydrate.base import Dehydrator
        return getattr(self.spec, 'dehydrator', Dehydrator)

    @property
    def specs(self):
        return getattr(self.spec, 'specs', ())


@registry.register('iterable')
class IterableNestedHandler(NestedHandler):

    def apply_dehydrator(self, dehydrator, target):
        return map(dehydrator.dehydrate, target)
