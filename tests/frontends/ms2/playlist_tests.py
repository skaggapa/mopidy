from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *
from mopidy.audio.mixers.utils import create_track

try:
    from mopidy.frontends.ms2 import playlist
    from mopidy.frontends.ms2 import item
    from mopidy.frontends.ms2.item import SpotifyItem
except exceptions.OptionalDependencyError:
    pass

from tests import unittest

OBJ_IFACE='org.gnome.UPnP.MediaObject2'
CONT_IFACE='org.gnome.UPnP.MediaContainer2'

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class PlayListTests(unittest.TestCase):
    def setUp(self):
        self.pl = create_playlist_mock()
        self.pl.tracks.append(create_track_mock())
        self.pl.tracks.append(create_track_mock())
        self.parent=create_parent_mock()
        dbus.service = mock.Mock()
        dbus.service.Object = mock.Mock()
        playlist.PlayList._connect_to_dbus = mock.Mock()
        playlist.PlayList.Updated = mock.Mock()
        self.plo = playlist.PlayList(self.parent, self.pl)
        
    def testConstructor1(self):
        self.assertTrue(self.plo._connect_to_dbus.called)
        self.assertTrue(self.plo.Updated.called)
        self.assertTrue(len(self.plo._props[OBJ_IFACE]),4)
        self.assertTrue(len(self.plo._props[CONT_IFACE]),4)


    def testConstructor2(self):
        dbus.service = mock.Mock()
        dbus.service.Object = mock.Mock()
        self.pl.tracks=[]
        playlist.PlayList._connect_to_dbus = mock.Mock()
        playlist.PlayList.Updated = mock.Mock()
        self.plo = playlist.PlayList(self.parent, self.pl)
        self.assertTrue(self.plo._connect_to_dbus.called)
        self.assertFalse(self.plo.Updated.called)
        self.assertTrue(len(self.plo._props[OBJ_IFACE]),4)
        self.assertTrue(len(self.plo._props[CONT_IFACE]),4)
        
        
    def test_constructor_3(self):
        tr = mock.Mock()
        tr.uri="spotify:12312akjdnakjsdn"
        tr.name="name 1"
        self.pl.tracks.append(tr)
        tr2 = mock.Mock()
        tr2.uri="spotify:asdmlakmd123123"
        tr2.name="name 2"
        self.pl.tracks.append(tr2)
        
        self.plo = playlist.PlayList(self.parent, self.pl)
        self.assertTrue(isinstance(self.plo._children[0], item.Item))
        self.assertTrue(isinstance(self.plo._children[1], item.Item))
        self.assertTrue(isinstance(self.plo._children[2], SpotifyItem))
        self.assertTrue(isinstance(self.plo._children[3], SpotifyItem))
    
    def test_item_selector1(self):
        item_ = mock.Mock()
        item_.uri="spotify:234234sdasda123123"
        ret = self.plo.item_selector(item_)
        self.assertTrue(isinstance(ret, SpotifyItem))


    def test_item_selector1(self):
        item_ = mock.Mock()
        item_.uri="/some/type/of/path"
        ret = self.plo.item_selector(item_)
        self.assertTrue(isinstance(ret, item.Item))

        