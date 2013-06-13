# coding: utf-8
from __future__ import unicode_literals

from mock import Mock

from dehydrate.fields import SimpleField


def test_is_relevant_one_element_string():
    assert SimpleField.is_relevant('username')


def test_is_relevant_two_elements_string():
    assert SimpleField.is_relevant(('username', 'name'))


def test_is_relevant_not_relevant_spec():
    assert not SimpleField.is_relevant(1)
    assert not SimpleField.is_relevant({'hello': 1})


def test_target_property():
    field = SimpleField(dehydrator=None, spec=None)

    field._target_info = 'name'

    assert field.target == 'name'


def test_build_value():
    field = SimpleField(dehydrator=None, spec=None)
    field.resolve_target = Mock(return_value='x')

    assert field.build_value(obj=None) == 'x'
