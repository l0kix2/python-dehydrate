# coding: utf-8
from __future__ import unicode_literals

from mock import Mock

from dehydrate.shortcuts import dehydrate


def test_dehydrate_shortcut_using_given_cls():
    fake_dehydrator_cls = Mock()

    dehydrate(obj=None, cls=fake_dehydrator_cls)

    fake_dehydrator_cls.assert_called_once_with(fields=None)


def test_dehydrate_shortcut_using_given_obj():
    fake_dehydrator_instance = Mock()
    fake_dehydrator_cls = Mock(**{
        'return_value': fake_dehydrator_instance
    })

    obj = None

    dehydrate(obj=obj, cls=fake_dehydrator_cls)

    fake_dehydrator_instance.dehydrate.assert_called_once_with(obj)
