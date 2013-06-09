# coding: utf-8
from __future__ import unicode_literals

from dehydrate import helpers


def test_wrap_in_dict():
    function = lambda: [('a', 1), ('b', 2)]
    function = helpers.wrap_in_dict(function)

    result = function()

    assert isinstance(result, dict)
    assert result.get('a') == 1
    assert result.get('b') == 2


def test_register_in_registry_doesnt_change_object():
    registry = helpers.Registry()
    func = lambda x: x

    wrapped_func = registry.register(func)

    assert func is wrapped_func


def test_registered_object_is_in_registry():
    registry = helpers.Registry()
    func = lambda x: x

    registry.register(func)

    assert func in registry._registry


def test_registry_is_iterable():
    registry = helpers.Registry()
    func = lambda x: x

    registry.register(func)

    assert func in registry
