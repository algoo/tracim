# -*- coding: utf-8 -*-

import datetime

from nose.tools import eq_
from nose.tools import ok_

import tracim.lib.helpers as h
from tracim.config.app_cfg import CFG
from tracim.model.data import Content
from tracim.model.data import ContentType
from tracim.model.data import Workspace

from tracim.model.serializers import Context
from tracim.model.serializers import CTX
from tracim.model.serializers import DictLikeClass

from tracim.tests import TestStandard


class TestHelpers(TestStandard):

    def test_is_item_still_editable(self):
        config = CFG.get_instance()
        item = DictLikeClass()

        config.DATA_UPDATE_ALLOWED_DURATION = 0
        item.created = datetime.datetime.now() - datetime.timedelta(0, 10)

        item.type = DictLikeClass({'id': 5})
        eq_(False, h.is_item_still_editable(config, item))

        item.type.id = 'comment'
        eq_(False, h.is_item_still_editable(config, item))

        config.DATA_UPDATE_ALLOWED_DURATION = -1
        item.type.id = 'comment'
        item.created = datetime.datetime.now() - datetime.timedelta(0, 10)
        eq_(True, h.is_item_still_editable(config, item))

        config.DATA_UPDATE_ALLOWED_DURATION = 12
        item.created = datetime.datetime.now() - datetime.timedelta(0, 10)
        eq_(True, h.is_item_still_editable(config, item), 'created: {}, now: {}'.format(item.created, datetime.datetime.now())) # This test will pass only if the test duration is less than 120s !!!

        config.DATA_UPDATE_ALLOWED_DURATION = 8
        item.created = datetime.datetime.now() - datetime.timedelta(0, 10)
        eq_(False, h.is_item_still_editable(config, item))
