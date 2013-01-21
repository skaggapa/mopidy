from __future__ import unicode_literals

import mock
from tests import unittest
import subprocess
import signal
import sys
import os
import dbus

ROOT_PATH='/org/gnome/UPnP/MediaServer2/mopidy'
SERVICE='org.gnome.UPnP.MediaServer2.mopidy'

PROP_IF='org.freedesktop.DBus.Properties'

OBJ_IF='org.gnome.UPnP.MediaObject2'
CONT_IF='org.gnome.UPnP.MediaContainer2'
ITEM_IF='org.gnome.UPnP.MediaItem2'

@unittest.skipUnless(False, 'requres linux, mopidy running and well defined local backend only')
class DBusTests(unittest.TestCase):
    def setUp(self):
        bus = dbus.SessionBus()
        self.root_obj = bus.get_object(SERVICE, ROOT_PATH)

    def smartCompare(self, res, expect):
        self.assertEqual(len(res),len(expect))
        for key in expect:
            if key != 'Path':
                self.assertEqual(res[key],expect[key])
        
    def testPropertiesObjectInterface1(self):
        prop_if=dbus.Interface(self.root_obj,dbus_interface=PROP_IF)
        #Object interface
        ret=prop_if.Get(OBJ_IF, 'Type')
        self.assertEqual(ret,'container')
        ret=prop_if.Get(OBJ_IF, 'Parent')
        self.assertEqual(ret,ROOT_PATH)
        ret=prop_if.Get(OBJ_IF, 'Path')
        self.assertEqual(ret,ROOT_PATH)
        ret=prop_if.Get(OBJ_IF, 'DisplayName')
        self.assertEqual(ret,'mopidy')

    def testPropertiesContainerInterface1(self):
        prop_if=dbus.Interface(self.root_obj,dbus_interface=PROP_IF)
        #Container interface
        ret=prop_if.Get(CONT_IF, 'ChildCount')
        self.assertEqual(ret,2)
        ret=prop_if.Get(CONT_IF, 'ContainerCount')
        self.assertEqual(ret,2)
        ret=prop_if.Get(CONT_IF, 'ItemCount')
        self.assertEqual(ret,0)
        ret=prop_if.Get(CONT_IF, 'Searchable')
        self.assertEqual(ret,False)

    def testListChildren1(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListChildren(0,0,['*'])
        self.assertEqual(len(ret),2)
        print ret[0]['DisplayName']
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})
        self.smartCompare(ret[1], {'DisplayName': 'bryan adams - unplugged',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})

    def testListChildren2(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListChildren(0,0,['Path', 'ItemCount'])
        self.assertEqual(len(ret),2)
        self.smartCompare(ret[0], {'Path': 'dummy',
                                   'ItemCount': 4})
        self.smartCompare(ret[1], {'Path': 'dummy',
                                   'ItemCount': 4})

    def testListChildren3(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListChildren(0,1,['*'])
        self.assertEqual(len(ret),1)
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})

    def testListChildren4(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListChildren(1,0,['*'])
        print ret
        self.assertEqual(len(ret),1)
        self.smartCompare(ret[0], {'DisplayName': 'bryan adams - unplugged',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})        

    def testListChildren5(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListChildren(1,0,['Parent', 'Path'])
        print ret
        self.assertEqual(len(ret),1)
        self.smartCompare(ret[0], {'Parent': ROOT_PATH,
                                   'Path': 'dummy'})        

    def testListContainers1(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,0,['*'])
        self.assertEqual(len(ret),2)
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})
        self.smartCompare(ret[1], {'DisplayName': 'bryan adams - unplugged',
                                   'Parent': ROOT_PATH,
                                   'Path': 'dummy',
                                   'Type': 'container',
                                   'ChildCount': 4,
                                   'ItemCount': 4,
                                   'ContainerCount': 0,
                                   'Searchable': False})        
    
    def testListContainers2(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,0,['DisplayName'])
        self.assertEqual(len(ret),2)
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations'})
        self.smartCompare(ret[1], {'DisplayName': 'bryan adams - unplugged'})
        
    def testListContainers3(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,0,['DisplayName', 'Type'])
        self.assertEqual(len(ret),2)
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations',
                                   'Type': 'container'})
        self.smartCompare(ret[1], {'DisplayName': 'bryan adams - unplugged',
                                   'Type': 'container'})

    def testListContainers4(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(1,0,['DisplayName', 'Type'])
        self.assertEqual(len(ret),1)
        self.smartCompare(ret[0], {'DisplayName': 'bryan adams - unplugged',
                                   'Type': 'container'})

    def testListContainers5(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,1,['DisplayName', 'Type'])
        self.assertEqual(len(ret),1)
        self.smartCompare(ret[0], {'DisplayName': 'audioslave - revelations',
                                   'Type': 'container'})
    
    def testListItems1(self):
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListItems(0,0,['*'])
        self.assertEqual(len(ret),0)

    def testListItems2(self):
        # Ge a child for easier testing
        bus=dbus.SessionBus()
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,1,['Path'])
        cont_obj=bus.get_object(SERVICE,ret[0]['Path'])
        cont_if=dbus.Interface(cont_obj, dbus_interface=CONT_IF)
        ret=cont_if.ListItems(0,0,['DisplayName'])
        self.assertEqual(len(ret),4)
        self.smartCompare(ret[0], {'DisplayName': 'Revelations'})
        self.smartCompare(ret[1], {'DisplayName': 'One And The Same'})
        self.smartCompare(ret[2], {'DisplayName': 'Sound Of A Gun'})
        self.smartCompare(ret[3], {'DisplayName': 'Until We Fall'})

    def testListItems3(self):
        # Ge a child for easier testing
        bus=dbus.SessionBus()
        cont_if=dbus.Interface(self.root_obj,dbus_interface=CONT_IF)
        ret=cont_if.ListContainers(0,1,['Path'])
        cont_obj=bus.get_object(SERVICE,ret[0]['Path'])
        cont_if=dbus.Interface(cont_obj, dbus_interface=CONT_IF)
        ret=cont_if.ListItems(1,2,['DisplayName'])
        self.assertEqual(len(ret),2)
        self.smartCompare(ret[0], {'DisplayName': 'One And The Same'})
        self.smartCompare(ret[1], {'DisplayName': 'Sound Of A Gun'})
