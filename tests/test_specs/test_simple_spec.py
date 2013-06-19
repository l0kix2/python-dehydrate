# coding: utf-8
from __future__ import unicode_literals

from mock import Mock

from dehydrate.specs import SimpleSpec


def test_is_relevant_one_element_string():
    assert SimpleSpec.is_relevant('username')


def test_is_relevant_two_elements_string():
    assert SimpleSpec.is_relevant(('username', 'name'))


def test_is_relevant_not_relevant_spec():
    assert not SimpleSpec.is_relevant(1)
    assert not SimpleSpec.is_relevant({'hello': 1})


def test_target_property():
    spec = SimpleSpec(dehydrator=None, spec=None)

    spec._target_info = 'name'

    assert spec.target == 'name'


def test_build_value():
    spec = SimpleSpec(dehydrator=None, spec=None)
    spec.resolve_target = Mock(return_value='x')

    assert spec.build_value(obj=None) == 'x'
