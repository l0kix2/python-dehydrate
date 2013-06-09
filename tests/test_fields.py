# coding: utf-8
from __future__ import unicode_literals

from mock import Mock
import pytest

from dehydrate.fields import Field, SimpleField, ComplexField
from dehydrate.exceptions import DehydrationException, SpecParsingError

from . import Initer


def test_parse_spec_with_one_element_spec():
    field = Field(dehydrator=None, spec='username')

    target_info, substitute = field.parse_spec()

    assert target_info == 'username'
    assert substitute is None


def test_parse_spec_with_two_element_spec():
    field = Field(dehydrator=None, spec=('username', 'login'))

    target_info, substitute = field.parse_spec()

    assert target_info == 'username'
    assert substitute == 'login'


def test_parse_spec_with_failing_validation():
    field = Field(dehydrator=None, spec='username')

    field.validate_target_info = Mock(side_effect=Exception)

    with pytest.raises(SpecParsingError):
        field.parse_spec()


def test_resolve_target_dehydrator_getter():
    dehydrator = Mock(**{
        'GETTER_PREFIX': 'get_',
        'get_username': lambda: 'batman',
    })
    field = Field(dehydrator=dehydrator, spec='username')
    obj = Initer(username='joker')

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'batman'


def test_resolve_target_object_attribute():
    field = Field(dehydrator=None, spec='username')
    field.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Initer(username='joker')

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'joker'


def test_resolve_target_object_method():
    field = Field(dehydrator=None, spec='username')
    field.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Mock(**{'username.return_value': 'joker'})

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'joker'


def test_resolve_target_object_method():
    field = Field(dehydrator=None, spec='username')
    field.dehydrator = Initer(GETTER_PREFIX='get_')

    with pytest.raises(DehydrationException):
        field.resolve_target(obj=None, target_name='username')
