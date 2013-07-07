# coding: utf-8
"""
Tests for base.Dehydrator class.
"""
from __future__ import unicode_literals

from mock import Mock, patch, call
from pytest import raises

from dehydrate import Dehydrator, S
from dehydrate.exceptions import DehydrationException


# constants with DUMMY_* names instead of strings used for explicitly pointing,
# that their value is not important in this test.
DUMMY_OBJECT = object()
DUMMY_SPECS = ['name', 'age']  # simplified format
DUMMY_SINGLE_SPEC = DUMMY_SPECS[0]


# tests of methods in declaration order
def test_base_dehydrator_init():
    assert Dehydrator().specs == ()
    assert Dehydrator(specs=DUMMY_SPECS).specs == DUMMY_SPECS


def test_inheritor_init():
    class PersonDehydrator(Dehydrator):
        specs = DUMMY_SPECS

    assert PersonDehydrator().specs == DUMMY_SPECS

    DUMMY_SPECS_EXTENDED = DUMMY_SPECS + ['login']
    redefined_specs = PersonDehydrator(specs=DUMMY_SPECS_EXTENDED).specs
    assert redefined_specs == DUMMY_SPECS_EXTENDED


@patch('dehydrate.base.Dehydrator.dehydrate_spec')
def test_dehydrate(dehydrate_spec_mock):
    # TODO: find out how to undecorate function with mock
    dehydrate_spec_mock.return_value = zip(DUMMY_SPECS, ('Tummy', 10))

    dehydrator = Dehydrator()
    dehydrator.specs = DUMMY_SPECS

    dehydrator.dehydrate(obj=DUMMY_OBJECT)

    dehydrate_spec_mock.has_calls(
        call(DUMMY_OBJECT, DUMMY_SPECS[0]),
        call(DUMMY_OBJECT, DUMMY_SPECS[1]),
    )


def test_wrap_spec_if_needed_str():
    dehydrator = Dehydrator()

    wrapped = dehydrator.wrap_spec_if_needed(spec='login')

    assert isinstance(wrapped, S)
    assert wrapped.target == 'login'


def test_wrap_spec_if_needed_two_str_tuple():
    dehydrator = Dehydrator()

    wrapped = dehydrator.wrap_spec_if_needed(spec=('login', 'username'))

    assert isinstance(wrapped, S)
    assert wrapped.target == 'login'
    assert wrapped.substitution == 'username'


def test_wrap_spec_if_needed_S():
    dehydrator = Dehydrator()

    spec = S('login')
    wrapped = dehydrator.wrap_spec_if_needed(spec=spec)

    assert wrapped is spec


def test_wrap_spec_if_needed_wrong_type():
    dehydrator = Dehydrator()

    with raises(DehydrationException):
        dehydrator.wrap_spec_if_needed(spec={'wrong': 'type'})


@patch('dehydrate.base.Dehydrator.select_handler')
@patch('dehydrate.base.Dehydrator.wrap_spec_if_needed', lambda self, x: x)
def test_dehydrate_spec(select_handler):
    select_handler.return_value = handler = Mock()
    dehydrator = Dehydrator()

    dehydrator.dehydrate_spec(obj=DUMMY_OBJECT, spec=DUMMY_SINGLE_SPEC)

    select_handler.assert_called_once_with(DUMMY_SINGLE_SPEC)
    handler.build_key.assert_called_once_with()
    handler.build_value.assert_called_once_with(DUMMY_OBJECT)


@patch('dehydrate.base.handlers')
def test_select_handler_found_in_registry(handlers_module):
    dehydrator = Dehydrator()
    spec_handler_cls = Mock()
    handlers_module.registry = {'simple': spec_handler_cls}
    spec = Mock(type='simple')

    dehydrator.select_handler(spec=spec)

    spec_handler_cls.assert_called_once_with(spec=spec, dehydrator=dehydrator)


@patch('dehydrate.base.handlers')
def test_select_handler_not_found_in_registry(handlers_module):
    dehydrator = Dehydrator()
    spec_handler_cls = Mock()
    handlers_module.registry = {'simple': spec_handler_cls}
    spec = Mock(type='unknown')

    with raises(DehydrationException):
        dehydrator.select_handler(spec=spec)
