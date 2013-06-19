# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, call
import pytest

from dehydrate import Dehydrator
from dehydrate.specs import ComplexSpec
from dehydrate.exceptions import DehydrationException


def test_is_relevant_one_element_dict():
    assert ComplexSpec.is_relevant(
        {'specs': ('username',)}
    )


def test_is_relevant_two_elements_string():
    assert ComplexSpec.is_relevant((
        {'specs': ('username',)},
        'name'
    ))


def test_is_relevant_not_relevant_spec():
    assert not ComplexSpec.is_relevant(1)
    assert not ComplexSpec.is_relevant('username')


def test_target_property():
    spec = ComplexSpec(dehydrator=None, spec=None)

    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username'
    }

    assert spec.target == 'username'


def test_is_iterable_property():
    spec = ComplexSpec(dehydrator=None, spec=None)

    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username',
    }

    assert not spec.is_iterable

    spec._target_info[ComplexSpec.ITERABLE_FLAG_FIELD_NAME] = True

    assert spec.is_iterable


def test_dehydrator_cls_property():
    spec = ComplexSpec(dehydrator=None, spec=None)

    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username',
    }

    assert spec.dehydrator_cls is Dehydrator

    spec._target_info[ComplexSpec.DEHYDRATOR_FIELD_NAME] = object

    assert spec.dehydrator_cls is object


def test_specs_property():
    spec = ComplexSpec(dehydrator=None, spec=None)

    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username',
        'specs': ('a', 'b')
    }

    assert spec.specs == ('a', 'b')


def test_build_value_for_not_iterable():
    spec = ComplexSpec(dehydrator=None, spec=None)
    spec.resolve_target = Mock(return_value='x')
    dehydrator = Mock()
    dehydrator_cls = Mock(return_value=dehydrator)
    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username',
        ComplexSpec.DEHYDRATOR_FIELD_NAME: dehydrator_cls
    }

    spec.build_value(obj=None)

    dehydrator.dehydrate.assert_called_once_with('x')


def test_build_value_for_iterable():
    spec = ComplexSpec(dehydrator=None, spec=None)
    spec.resolve_target = Mock(return_value=['a', 'b'])
    dehydrator = Mock()
    dehydrator_cls = Mock(return_value=dehydrator)
    spec._target_info = {
        ComplexSpec.TARGET_FIELD_NAME: 'username',
        ComplexSpec.DEHYDRATOR_FIELD_NAME: dehydrator_cls,
        ComplexSpec.ITERABLE_FLAG_FIELD_NAME: True
    }

    spec.build_value(obj=None)

    dehydrator.dehydrate.has_calls([call('a'), call('b')])


def test_validate_target_info():
    with pytest.raises(DehydrationException):
        ComplexSpec.validate_target_info({})

    ComplexSpec.validate_target_info({'target': 'username'})
