from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *
try:
    from mopidy.frontends.ms2 import abstractitem
except exceptions.OptionalDependencyError:
    pass

from tests import unittest

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class AbstractItemOTests(unittest.TestCase):
    def setUp(self):
        self.parent=create_parent_mock()
        self.item=create_item_mock()
        self.aio=abstractitem.AbstractItem(self.parent, self.item)
        
    def test_constructor1(self):
        self.assertEqual(self.aio._props[OBJ_IFACE]['DisplayName'],self.item.name)
        self.assertEqual(self.aio._props[OBJ_IFACE]['Type'],'audio')
        self.assertEqual(self.aio._props[ITEM_IFACE]['URLs'],[self.item.uri])
        self.assertEqual(self.aio._props[ITEM_IFACE]['MIMEType'],'mp3')