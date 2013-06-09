# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, patch
import pytest

from dehydrate.fields import Field, SimpleField, ComplexField
from dehydrate.exceptions import DehydrationException, SpecParsingError

from . import Initer


@patch('dehydrate.fields.Field.parse_spec')
def test_parse_spec_is_called_in_init(fake_parse_spec):
    fake_parse_spec.return_value = (None, None)

    Field(dehydrator=None, spec=None)

    fake_parse_spec.assert_called_once_with(spec=None)


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_parse_spec_with_one_element_spec():
    field = Field()

    target_info, substitute = field.parse_spec(spec='username')

    assert target_info == 'username'
    assert substitute is None


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_parse_spec_with_two_element_spec():
    field = Field()

    target_info, substitute = field.parse_spec(spec=('username', 'login'))

    assert target_info == 'username'
    assert substitute == 'login'


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_parse_spec_with_failing_validation():
    field = Field()

    field.validate_target_info = Mock(side_effect=Exception)

    with pytest.raises(SpecParsingError):
        field.parse_spec(spec='username')


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_resolve_target_dehydrator_getter():
    field = Field()
    field.dehydrator = Mock(**{
        'GETTER_PREFIX': 'get_',
        'get_username': lambda: 'batman',
    })
    obj = Initer(username='joker')

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'batman'


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_resolve_target_object_attribute():
    field = Field()
    field.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Initer(username='joker')

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'joker'


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_resolve_target_object_method():
    field = Field()
    field.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Mock(**{'username.return_value': 'joker'})

    getter = field.resolve_target(obj=obj, target_name='username')

    assert getter() == 'joker'


@patch('dehydrate.fields.Field.__init__', Mock(return_value=None))
def test_resolve_target_object_method():
    field = Field()
    field.dehydrator = Initer(GETTER_PREFIX='get_')

    with pytest.raises(DehydrationException):
        field.resolve_target(obj=None, target_name='username')

