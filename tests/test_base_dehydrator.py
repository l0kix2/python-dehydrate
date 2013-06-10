# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, patch

from dehydrate import Dehydrator


class TestDehydrator(Dehydrator):
    fields = ('name', 'age',)


def test_dehydrator_init():
    assert Dehydrator().fields == ()
    assert TestDehydrator().fields == ('name', 'age',)
    assert Dehydrator(fields=('name', 'login')).fields == ('name', 'login')


@patch(
    'dehydrate.base.Dehydrator.dehydrate_field',
    Mock(side_effect=[('name', 'batman'), ('age', 22)]),
)
def test_dehydrate():
    dehydrator = Dehydrator()
    dehydrator.fields = ('whatever', 'whatever')

    result = dehydrator.dehydrate(obj=None)

    assert result == {'name': 'batman', 'age': 22}


@patch('dehydrate.base.Dehydrator.wrap_field')
def test_dehydrate_field(wrap_func_mock):
    dehydrator = Dehydrator()
    field = Mock()
    wrap_func_mock.return_value = field

    dehydrator.dehydrate_field(obj='obj', spec='spec')

    wrap_func_mock.assert_called_once_with('spec')
    field.build_key.assert_called_once_with()
    field.build_value.assert_called_once_with('obj')


@patch('dehydrate.base.fields')
def test_wrap_field_no_relevant(fields_module_mock):
    field_cls_1 = Mock(**{'is_relevant.return_value': False})
    field_cls_2 = Mock(**{'is_relevant.return_value': False})

    fields_module_mock.registry = [field_cls_1, field_cls_2]
    dehydrator = Dehydrator()

    dehydrator.wrap_field(spec='spec')

    field_cls_1.is_relevant.assert_called_once_with('spec')
    field_cls_2.is_relevant.assert_called_once_with('spec')
    assert field_cls_1.call_count == 0
    assert field_cls_2.call_count == 0


@patch('dehydrate.base.fields')
def test_wrap_field_no_relevant(fields_module_mock):
    field_cls_1 = Mock(**{'is_relevant.return_value': True})
    field_cls_2 = Mock(**{'is_relevant.return_value': False})

    fields_module_mock.registry = [field_cls_1, field_cls_2]
    dehydrator = Dehydrator()

    dehydrator.wrap_field(spec='spec')

    field_cls_1.is_relevant.assert_called_once_with('spec')
    field_cls_1.assert_called_once_with(dehydrator=dehydrator, spec='spec')
    assert field_cls_2.call_count == 0
