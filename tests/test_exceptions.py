# coding: utf-8
from __future__ import unicode_literals

from pretend import stub

from dehydrate.exceptions import (
    DehydrationException,
    TargetResolvingError,
)


def test_dehydration_exception_init():
    stap = 'Wow-wow-wow, make it stap'
    exc = DehydrationException(
        description=stap,
        why='its failed',
    )

    assert hasattr(exc, 'why')
    assert exc.why == 'its failed'
    assert exc.description == stap


def test_exception_str():
    exc = DehydrationException(description='Some Error')
    assert str(exc) == 'Some Error'


def test_exception_unicode():
    exc = DehydrationException(description='Some Error')
    # TODO: py3 hacks. mark tests for py2
    assert exc.__unicode__() == 'Some Error'


def test_exception_repr():
    exc = DehydrationException(description='Some Error')
    assert repr(exc) == 'Some Error'


def test_description_tpl():
    template = 'Something happened. Look at this {string} and {number}'
    exc = DehydrationException(
        description_tpl=template,
        string='spam',
        number=42,
    )

    assert str(exc) == 'Something happened. Look at this spam and 42'


def test_target_resolving_error():
    person = stub(login='iron_man', full_name=lambda: 'Tony Stark')
    dehydrator = stub(get_username=lambda x: x)

    DUMMY_TARGET = 'WHATEVER'
    exc = TargetResolvingError(
        target=DUMMY_TARGET,
        obj=person,
        dehydrator=dehydrator,
    )

    assert 'login' in exc.object_attributes_string
    assert 'full_name' in exc.object_methods_string
    assert 'get_username' in exc.dehydrator_getters_string
