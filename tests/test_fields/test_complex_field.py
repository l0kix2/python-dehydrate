# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, call
import pytest

from dehydrate import Dehydrator
from dehydrate.fields import ComplexField
from dehydrate.exceptions import DehydrationException


def test_is_relevant_one_element_dict():
    assert ComplexField.is_relevant(
        {'fields': ('username',)}
    )


def test_is_relevant_two_elements_string():
    assert ComplexField.is_relevant((
        {'fields': ('username',)},
        'name'
    ))


def test_is_relevant_not_relevant_spec():
    assert not ComplexField.is_relevant(1)
    assert not ComplexField.is_relevant('username')


def test_target_property():
    field = ComplexField(dehydrator=None, spec=None)

    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username'
    }

    assert field.target == 'username'


def test_is_iterable_property():
    field = ComplexField(dehydrator=None, spec=None)

    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username',
    }

    assert not field.is_iterable

    field._target_info[ComplexField.ITERABLE_FLAG_FIELD_NAME] = True

    assert field.is_iterable


def test_dehydrator_cls_property():
    field = ComplexField(dehydrator=None, spec=None)

    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username',
    }

    assert field.dehydrator_cls is Dehydrator

    field._target_info[ComplexField.DEHYDRATOR_FIELD_NAME] = object

    assert field.dehydrator_cls is object


def test_field_property():
    field = ComplexField(dehydrator=None, spec=None)

    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username',
        'fields': ('a', 'b')
    }

    assert field.fields == ('a', 'b')


def test_build_value_for_not_iterable():
    field = ComplexField(dehydrator=None, spec=None)
    field.resolve_target = Mock(return_value='x')
    dehydrator = Mock()
    dehydrator_cls = Mock(return_value=dehydrator)
    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username',
        ComplexField.DEHYDRATOR_FIELD_NAME: dehydrator_cls
    }

    field.build_value(obj=None)

    dehydrator.dehydrate.assert_called_once_with('x')


def test_build_value_for_iterable():
    field = ComplexField(dehydrator=None, spec=None)
    field.resolve_target = Mock(return_value=['a', 'b'])
    dehydrator = Mock()
    dehydrator_cls = Mock(return_value=dehydrator)
    field._target_info = {
        ComplexField.TARGET_FIELD_NAME: 'username',
        ComplexField.DEHYDRATOR_FIELD_NAME: dehydrator_cls,
        ComplexField.ITERABLE_FLAG_FIELD_NAME: True
    }

    field.build_value(obj=None)

    dehydrator.dehydrate.has_calls([call('a'), call('b')])


def test_validate_target_info():
    with pytest.raises(DehydrationException):
        ComplexField.validate_target_info({})

    ComplexField.validate_target_info({'target': 'username'})
