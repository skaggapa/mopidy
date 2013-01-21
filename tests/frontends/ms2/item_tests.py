from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *
try:
    from mopidy.frontends.ms2 import item
except exceptions.OptionalDependencyError:
    pass

from tests import unittest

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class ItemTests(unittest.TestCase):
    def setUp(self):
        dbus.service=mock.Mock()
        self.parent = create_parent_mock()
        self.item = create_item_mock()
        self.io = item.Item(self.parent, self.item)

    def testContstructor1(self):
        dbus.service=mock.Mock()
        item.Item._connect_to_dbus = mock.Mock()
        io = item.Item(self.parent, self.item)
        self.assertTrue(io._connect_to_dbus.called)