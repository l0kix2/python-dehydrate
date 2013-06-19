# coding: utf-8
from __future__ import unicode_literals

from mock import Mock
import pytest

from dehydrate.specs import Spec
from dehydrate.exceptions import DehydrationException

from .. import Initer


def test_parse_spec_with_one_element_spec():
    spec = Spec(dehydrator=None, spec='username')

    target_info, substitute = spec.parse_spec()

    assert target_info == 'username'
    assert substitute is None


def test_parse_spec_with_two_element_spec():
    spec = Spec(dehydrator=None, spec=('username', 'login'))

    target_info, substitute = spec.parse_spec()

    assert target_info == 'username'
    assert substitute == 'login'


def test_parse_spec_with_failing_validation():
    spec = Spec(dehydrator=None, spec='username')

    spec.validate_target_info = Mock(side_effect=Exception)

    with pytest.raises(DehydrationException):
        spec.parse_spec()


def test_resolve_target_with_dehydrator_getter():
    class TestDehydrator(object):
        GETTER_PREFIX = 'get_'

        def get_username(self, obj):
            return 'batman'

    spec = Spec(dehydrator=TestDehydrator(), spec='username')
    obj = Initer(username='joker')

    target = spec.resolve_target(obj=obj, target_name='username')

    assert target == 'batman'


def test_resolve_target_object_attribute():
    spec = Spec(dehydrator=None, spec='username')
    spec.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Initer(username='joker')

    target = spec.resolve_target(obj=obj, target_name='username')

    assert target == 'joker'


def test_resolve_target_object_method():
    spec = Spec(dehydrator=None, spec=None)
    spec.dehydrator = Initer(GETTER_PREFIX='get_')
    obj = Mock(**{'username.return_value': 'joker'})

    target = spec.resolve_target(obj=obj, target_name='username')

    assert target == 'joker'


def test_resolve_target_cant_be_resolved():
    spec = Spec(dehydrator=None, spec='username')
    spec.dehydrator = Initer(GETTER_PREFIX='get_')

    with pytest.raises(DehydrationException):
        spec.resolve_target(obj=None, target_name='username')


def test_target_info():
    spec = Spec(dehydrator=None, spec=None)
    spec.parse_spec = Mock(return_value=('a', 'b'))

    assert spec.target_info == 'a'
    spec.target_info  # second call

    spec.parse_spec.assert_called_once()


def test_substitution():
    spec = Spec(dehydrator=None, spec=None)
    spec.parse_spec = Mock(return_value=('a', 'b'))

    assert spec.substitution == 'b'
    spec.substitution  # second call

    spec.parse_spec.assert_called_once()


def test_build_key_if_substitution():
    spec = Spec(dehydrator=None, spec=None)

    spec._substitution = 'a'

    assert spec.build_key() == 'a'


def test_not_implemented_in_base_class():
    with pytest.raises(NotImplementedError):
        Spec.is_relevant(spec='whatever')
