# coding: utf-8
from __future__ import unicode_literals

from mock import Mock

from dehydrate.shortcuts import dehydrate


DUMMY_OBJECT = object()
DUMMY_SPECS = ('name', 'login')  # simplified format


# some mock helpers for readability
def get_dehydrator():
    fake_dehydrator_instance = Mock()
    fake_dehydrator_cls = Mock(return_value=fake_dehydrator_instance)
    return fake_dehydrator_cls, fake_dehydrator_instance


def assert_callable_called(callable, *args, **kwargs):
    callable.assert_called_once_with(*args, **kwargs)


def assert_class_initialized(cls, *args, **kwargs):
    assert_callable_called(cls, *args, **kwargs)


# tests
def test_dehydrate_shortcut_using_given_cls_without_specs():
    cls, instance = get_dehydrator()

    dehydrate(obj=DUMMY_OBJECT, cls=cls)

    assert_class_initialized(cls=cls, specs=None, empty=None)
    assert_callable_called(callable=instance.dehydrate, obj=DUMMY_OBJECT)


def test_dehydrate_shortcut_using_given_cls_with_specs():
    cls, instance = get_dehydrator()

    dehydrate(obj=DUMMY_OBJECT, cls=cls, specs=DUMMY_SPECS)

    assert_class_initialized(cls=cls, specs=DUMMY_SPECS, empty=None)
    assert_callable_called(callable=instance.dehydrate, obj=DUMMY_OBJECT)


def test_dehydrate_shortcut_using_given_obj_without_specs():
    cls, instance = get_dehydrator()

    dehydrate(obj=DUMMY_OBJECT, cls=cls)

    assert_class_initialized(cls=cls, specs=None, empty=None)
    assert_callable_called(callable=instance.dehydrate, obj=DUMMY_OBJECT)


def test_dehydrate_shortcut_using_given_obj_with_specs():
    cls, instance = get_dehydrator()

    dehydrate(obj=DUMMY_OBJECT, cls=cls, specs=DUMMY_SPECS)

    assert_class_initialized(cls=cls, specs=DUMMY_SPECS, empty=None)
    assert_callable_called(callable=instance.dehydrate, obj=DUMMY_OBJECT)
