# coding: utf-8
from __future__ import unicode_literals

from pretend import stub
import pytest

from dehydrate.handlers import Handler
from dehydrate.exceptions import DehydrationException


DUMMY_SPEC = object()
DUMMY_OBJECT = object()


def test_target_property():
    spec = stub(target='login')
    handler = Handler(dehydrator=DUMMY_OBJECT, spec=spec)

    assert handler.target == 'login'


def test_resolve_target_with_dehydrator_getter():
    class PersonDehydrator(object):
        GETTER_PREFIX = 'get_'

        def get_username(self, obj):
            return 'batman'

    handler = Handler(dehydrator=PersonDehydrator(), spec=DUMMY_SPEC)
    obj = stub(username='joker')

    target = handler.resolve_target(obj=obj, target='username')

    assert target == 'batman'


def test_resolve_target_object_attribute():
    handler = Handler(dehydrator=None, spec=DUMMY_SPEC)
    handler.dehydrator = stub(GETTER_PREFIX='get_')
    obj = stub(username='joker')

    target = handler.resolve_target(obj=obj, target='username')

    assert target == 'joker'


def test_resolve_target_object_method():
    handler = Handler(dehydrator=None, spec=None)
    handler.dehydrator = stub(GETTER_PREFIX='get_')
    obj = stub(username=lambda: 'joker')

    target = handler.resolve_target(obj=obj, target='username')

    assert target == 'joker'


def test_resolve_target_cant_be_resolved():
    handler = Handler(dehydrator=None, spec=DUMMY_SPEC)
    handler.dehydrator = stub(GETTER_PREFIX='get_')

    with pytest.raises(DehydrationException):
        handler.resolve_target(obj=DUMMY_OBJECT, target='username')


def test_build_key_if_substitution():
    spec = stub(target='login', substitution='username')
    handler = Handler(dehydrator=DUMMY_OBJECT, spec=spec)

    assert handler.build_key() == 'username'


def test_build_key_if_no_substitution():
    spec = stub(target='login', substitution=None)
    handler = Handler(dehydrator=DUMMY_OBJECT, spec=spec)

    assert handler.build_key() == 'login'
