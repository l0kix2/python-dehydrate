# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, patch

from dehydrate import Dehydrator


class TestDehydrator(Dehydrator):
    specs = ('name', 'age',)


def test_dehydrator_init():
    assert Dehydrator().specs == ()
    assert TestDehydrator().specs == ('name', 'age',)
    assert Dehydrator(specs=('name', 'login')).specs == ('name', 'login')


@patch(
    'dehydrate.base.Dehydrator.dehydrate_spec',
    Mock(side_effect=[('name', 'batman'), ('age', 22)]),
)
def test_dehydrate():
    dehydrator = Dehydrator()
    dehydrator.specs = ('whatever', 'whatever')

    result = dehydrator.dehydrate(obj=None)

    assert result == {'name': 'batman', 'age': 22}


@patch('dehydrate.base.Dehydrator.wrap_spec')
def test_dehydrate_spec(wrap_func_mock):
    dehydrator = Dehydrator()
    spec = Mock()
    wrap_func_mock.return_value = spec

    dehydrator.dehydrate_spec(obj='obj', spec='spec')

    wrap_func_mock.assert_called_once_with('spec')
    spec.build_key.assert_called_once_with()
    spec.build_value.assert_called_once_with('obj')


@patch('dehydrate.base.specs')
def test_wrap_spec_no_relevant(specs_module_mock):
    spec_cls_1 = Mock(**{'is_relevant.return_value': False})
    spec_cls_2 = Mock(**{'is_relevant.return_value': False})

    specs_module_mock.registry = [spec_cls_1, spec_cls_2]
    dehydrator = Dehydrator()

    dehydrator.wrap_spec(spec='spec')

    spec_cls_1.is_relevant.assert_called_once_with('spec')
    spec_cls_2.is_relevant.assert_called_once_with('spec')
    assert spec_cls_1.call_count == 0
    assert spec_cls_2.call_count == 0


@patch('dehydrate.base.specs')
def test_wrap_spec_no_relevant(specs_module_mock):
    spec_cls_1 = Mock(**{'is_relevant.return_value': True})
    apec_cls_2 = Mock(**{'is_relevant.return_value': False})

    specs_module_mock.registry = [spec_cls_1, apec_cls_2]
    dehydrator = Dehydrator()

    dehydrator.wrap_spec(spec='spec')

    spec_cls_1.is_relevant.assert_called_once_with('spec')
    spec_cls_1.assert_called_once_with(dehydrator=dehydrator, spec='spec')
    assert apec_cls_2.call_count == 0
