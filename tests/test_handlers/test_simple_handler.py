# coding: utf-8
from __future__ import unicode_literals

from mock import Mock, patch
from pretend import stub

from dehydrate.handlers import SimpleHandler

DUMMY_SPEC = object()
DUMMY_OBJECT = object()
DUMMY_TARGET = 'whatever'


@patch('dehydrate.handlers.SimpleHandler.target', DUMMY_TARGET)
@patch('dehydrate.handlers.SimpleHandler.resolve_target')
def test_build_value(resolve_target_mock):
    handler = SimpleHandler(dehydrator=DUMMY_OBJECT, spec=DUMMY_SPEC)

    handler.build_value(obj=DUMMY_OBJECT) == DUMMY_OBJECT

    resolve_target_mock.assert_called_once_with(
        obj=DUMMY_OBJECT, target=DUMMY_TARGET)


@patch('dehydrate.handlers.SimpleHandler.target', DUMMY_TARGET)
def test_post_hook():
    dehydrator = stub(post_handle_value=lambda obj: obj.upper())
    handler = SimpleHandler(dehydrator=dehydrator, spec=DUMMY_SPEC)
    handler.resolve_target = Mock(return_value='iron_man')

    assert handler.build_value(obj=DUMMY_OBJECT) == 'IRON_MAN'
