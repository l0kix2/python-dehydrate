# coding: utf-8
from __future__ import unicode_literals

from dehydrate.exceptions import DehydrationException


def test_dehydration_exception():
    stap = 'Wow-wow-wow, make it stap'
    exc = DehydrationException(
        description=stap,
        why='its failed',
    )

    assert exc.why == 'its failed'
    assert exc.description == stap
    assert str(exc) == stap
