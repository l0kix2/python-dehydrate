# coding: utf-8
from __future__ import unicode_literals

from mock import patch
from pretend import stub

from dehydrate.handlers import NestedHandler, IterableNestedHandler


DUMMY_OBJECT = object()
DUMMY_DEHYDRATOR = object()
DUMMY_SPECS = ('name', 'age')
DUMMY_SPEC = DUMMY_SPECS[0]
DUMMY_TARGET = 'whatever'


def test_dehydrator_cls_property():
    spec = stub(dehydrator=DUMMY_DEHYDRATOR)
    handler = NestedHandler(dehydrator=DUMMY_OBJECT, spec=spec)

    assert handler.dehydrator_cls is DUMMY_DEHYDRATOR


def test_specs_property():
    spec = stub(specs=DUMMY_SPECS)
    handler = NestedHandler(dehydrator=DUMMY_OBJECT, spec=spec)

    assert handler.specs is DUMMY_SPECS


# Ugly, ugly, ugly :(
@patch('dehydrate.handlers.NestedHandler.target', DUMMY_TARGET)
@patch('dehydrate.handlers.NestedHandler.dehydrator_cls')
@patch('dehydrate.handlers.NestedHandler.resolve_target')
@patch('dehydrate.handlers.NestedHandler.specs', DUMMY_SPECS)
@patch('dehydrate.handlers.NestedHandler.apply_dehydrator')
def test_nested_build_value(
        apply_dehydrator_mock,
        resolve_target_mock,
        dehydrator_cls_mock):
    handler = NestedHandler(dehydrator=DUMMY_OBJECT, spec=DUMMY_SPEC)
    resolve_target_mock.return_value = DUMMY_TARGET

    dehydrator_cls_mock.return_value = DUMMY_DEHYDRATOR

    handler.build_value(obj=None)

    dehydrator_cls_mock.assert_called_once_with(specs=DUMMY_SPECS)
    apply_dehydrator_mock.assert_called_once_with(
        DUMMY_DEHYDRATOR, DUMMY_TARGET)


def test_nested_apply_dehydrator():
    handler = NestedHandler(dehydrator=DUMMY_OBJECT, spec=DUMMY_SPEC)

    dehydrator = stub(dehydrate=lambda target: 'iron_man')
    result = handler.apply_dehydrator(
        dehydrator=dehydrator, target=DUMMY_TARGET)

    assert result == 'iron_man'


def test_iterable_apply_dehydrator():
    handler = IterableNestedHandler(dehydrator=DUMMY_OBJECT, spec=DUMMY_SPEC)

    dehydrator = stub(dehydrate=lambda str_value: str_value.upper())
    result = handler.apply_dehydrator(
        dehydrator=dehydrator, target=['iron_man', 'ir0n3000'])  # login/pass

    assert result == ['IRON_MAN', 'IR0N3000']
