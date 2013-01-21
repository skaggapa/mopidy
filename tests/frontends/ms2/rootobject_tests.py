from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *

try:
    from mopidy.frontends.ms2 import rootobject
    from mopidy.frontends.ms2 import playlist
except exceptions.OptionalDependencyError:
    pass

from tests import unittest

OBJ_IFACE='org.gnome.UPnP.MediaObject2'
CONT_IFACE='org.gnome.UPnP.MediaContainer2'
ROOT_PATH='/org/gnome/UPnP/MediaServer2/mopidy'

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class RootObjectTests(unittest.TestCase):
    def setUp(self):
        rootobject.exit_process = mock.Mock()
        self.core = mock.Mock()
        # mocked playlists in core
        self.mpl=[]
        self.core.playlists.playlists.get.return_value = self.mpl

    def testConstructor1(self):
        dbus.service=mock.Mock()
        rootobject.MediaServer2RootObject._connect_to_dbus = mock.Mock()
        rootobject.MediaServer2RootObject.Updated=mock.Mock()
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._connect_to_dbus.called)
        self.assertTrue(len(self.ro._children) == 0)
        self.assertFalse(self.ro.Updated.called)
        
    def testConstructor2(self):
        dbus.service=mock.Mock()
        rootobject.MediaServer2RootObject.Updated=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._connect_to_dbus.called)
        self.assertTrue(len(self.ro._children) == 2)
        self.assertTrue(self.ro.Updated.called)
        
    def test_obj_if_Properties(self):
        dbus.service=mock.Mock()
        self.ro = rootobject.MediaServer2RootObject(self.core)
        tmp = self.ro._props[OBJ_IFACE]
        
        self.assertEqual(tmp['Parent'], ROOT_PATH)
        self.assertEqual(tmp['Path'], ROOT_PATH)
        self.assertEqual(tmp['Type'], 'container')
        self.assertEqual(tmp['DisplayName'], 'mopidy')
        
    def test_cont_if_Properties(self):
        dbus.service=mock.Mock()
        self.ro = rootobject.MediaServer2RootObject(self.core)
        tmp = self.ro._props[CONT_IFACE]
        getter=tmp['ChildCount']
        res = getter() if callable(getter) else getter
        self.assertEqual(res, 0)
        getter=tmp['ItemCount']
        res = getter() if callable(getter) else getter
        self.assertEqual(res, 0)
        getter=tmp['ContainerCount']        
        res = getter() if callable(getter) else getter
        self.assertEqual(res, 0)
        getter=tmp['Searchable']
        self.assertEqual(res, False)

    def test_check_for_pl(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._check_for_pl(self.mpl[0]))
        self.assertFalse(self.ro._check_for_pl(create_playlist_mock()))

    def test_playlists_loaded(self):
        dbus.service=mock.Mock()
        rootobject.MediaServer2RootObject.Updated=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())

        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.ro.Updated.reset_mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro.playlists_loaded()
        self.assertTrue(self.ro.Updated.called)
        self.assertTrue(len(self.ro._children) == 5)
        self.assertEqual(self.ro.Updated.call_count, 3)
        
        self.ro.Updated.reset_mock()
        self.mpl.append(self.mpl[4])
        self.ro.playlists_loaded()
        self.assertFalse(self.ro.Updated.called)
        self.assertTrue(len(self.ro._children) == 5)
                
    def test_playlists_updated(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        playlist.PlayList._updated=mock.Mock()
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.ro._children=[]
        
        tmp=create_playlist_child_mock()
        self.ro._children.append(tmp)

        tmp=create_playlist_child_mock()
        self.ro._children.append(tmp)
        tmp1=mock.Mock()
        tmp1.uri=tmp._uri
        self.ro.playlists_updated(tmp1)

        self.assertTrue(self.ro._children[1]._updated.called)
        self.assertFalse(self.ro._children[0]._updated.called)

    def test_count_containers(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._count_containers()==2)
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro.playlists_loaded()
        self.assertTrue(self.ro._count_containers()==4)

    def test_count_children(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._count_children()==2)
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro.playlists_loaded()
        self.assertTrue(self.ro._count_children()==4)
               
    def test_count_items(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.assertTrue(self.ro._count_items()==0)
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro.playlists_loaded()
        self.assertTrue(self.ro._count_items()==0)
        
    def test_ListChildren2(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.ro._children[0]._query_props=mock.Mock()
        self.ro._children[0]._query_props.return_value={'Type':'container'}
        self.ro._children[1]._query_props=mock.Mock()
        self.ro._children[1]._query_props.return_value={'Type':'container'}
        self.ro._children[2]._query_props=mock.Mock()
        self.ro._children[2]._query_props.return_value={'Type':'container'}
        self.ro._children[3]._query_props=mock.Mock()
        self.ro._children[3]._query_props.return_value={'Type':'container'}        
        res = self.ro.ListChildren(0,0,'*')
        expect=[]
        expect.append({'Type':'container'})
        expect.append({'Type':'container'})
        expect.append({'Type':'container'})
        expect.append({'Type':'container'})
        self.assertEquals(res,expect)
        
    def test_ListContainers1(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.ro._children[0]._query_props=mock.Mock()
        self.ro._children[0]._query_props.return_value={'Type':'container 4'}
        self.ro._children[1]._query_props=mock.Mock()
        self.ro._children[1]._query_props.return_value={'Type':'container 3'}
        self.ro._children[2]._query_props=mock.Mock()
        self.ro._children[2]._query_props.return_value={'Type':'container 2'}
        self.ro._children[3]._query_props=mock.Mock()
        self.ro._children[3]._query_props.return_value={'Type':'container 1'}        
        res = self.ro.ListContainers(0,0,'*')
        expect=[]
        expect.append({'Type':'container 4'})
        expect.append({'Type':'container 3'})
        expect.append({'Type':'container 2'})
        expect.append({'Type':'container 1'})
        self.assertEquals(res,expect)
        
    def test_ListItems1(self):
        dbus.service=mock.Mock()
        self.mpl.append(create_playlist_mock())
        self.mpl.append(create_playlist_mock())
        self.ro = rootobject.MediaServer2RootObject(self.core)
        self.ro._children[0]._query_props=mock.Mock()
        self.ro._children[0]._query_props.return_value={'Type':'container 4'}
        self.ro._children[1]._query_props=mock.Mock()
        self.ro._children[1]._query_props.return_value={'Type':'container 3'}
        res = self.ro.ListItems(0,0,'*')
        expect=[]
        self.assertEquals(res,expect)
        
