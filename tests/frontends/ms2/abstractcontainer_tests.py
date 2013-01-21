from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *
try:
    from mopidy.frontends.ms2 import abstractcontainer
    from mopidy.frontends.ms2 import item

except exceptions.OptionalDependencyError:
    pass

from tests import unittest

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class AbstractContainerTests(unittest.TestCase):
    """ Could be extended to more of the methods, not 100 % 
    coverage
    
    """
    def setUp(self):
        dbus.service=mock.Mock()
        self.parent = create_parent_mock()
        self.aco = abstractcontainer.AbstractContainer(self.parent)
    
    def testConstructor1(self):
        self.assertEqual(self.aco._children, [])
        
    def test__count_children(self):
        self.aco._children.append(mock.Mock())
        self.aco._children.append(mock.Mock())
        self.aco._children.append(mock.Mock())
        self.assertEqual(self.aco._count_children(), 3)
        self.aco._children.append(mock.Mock())
        self.aco._children.append(mock.Mock())
        self.aco._children.append(mock.Mock())
        self.aco._children.append(mock.Mock())
        self.assertEqual(self.aco._count_children(), 7)
    
    def test__count_items(self):
        item.Item._connect_to_dbus = mock.Mock()
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.assertEqual(self.aco._count_items(), 3)
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        self.assertEqual(self.aco._count_items(), 3)

    def test__count_containers(self):
        item.Item._connect_to_dbus = mock.Mock()
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.assertEqual(self.aco._count_containers(), 0)
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        self.assertEqual(self.aco._count_containers(), 1)
        
    def test_properties(self):
        item.Item._connect_to_dbus = mock.Mock()
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(item.Item(self.parent, create_item_mock()))
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        self.assertEqual(self.aco._props[CONT_IFACE]['ChildCount'](), 4)
        self.assertEqual(self.aco._props[CONT_IFACE]['ItemCount'](), 3)
        self.assertEqual(self.aco._props[CONT_IFACE]['ContainerCount'](), 1)
        
    def test_ListChildren1(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock()
        self.aco._children.append(item.Item(self.parent, m))
        expect={'MIMEType': 'mp3',
                'DisplayName': 'mock',
                'Parent': '/mock/ed/path',
                'Type': 'audio'}
        self.assertEqual(len(self.aco.ListChildren(0, 0, ['*'])), 1)
        res = self.aco.ListChildren(0, 0, ['*'])
        self.assertTrue(self.smart_compare(res[0], expect))
    
    
    def test_ListChildren2(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
    
        self.assertEqual(len(self.aco.ListChildren(0, 0, ['*'])), 4)
        res=self.aco.ListChildren(0, 0, ['*'] )
        self.assertEqual(res[0]['DisplayName'], 'rock')
        self.assertEqual(res[1]['DisplayName'], 'pop')
        self.assertEqual(res[2]['DisplayName'], 'metal')
        self.assertEqual(res[3]['DisplayName'], 'techno')

    def test_ListChildren3(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        
        res = self.aco.ListChildren(2, 0, ['*'])
        self.assertEqual(len(self.aco.ListChildren(2, 0, ['*'])), 2)
        self.assertEqual(res[0]['DisplayName'], 'metal')
        self.assertEqual(res[1]['DisplayName'], 'techno')
    
    def test_ListChildren4(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        
        res=self.aco.ListChildren(1, 2, ['*'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['DisplayName'], 'pop')
        self.assertEqual(res[1]['DisplayName'], 'metal')

    def test_ListChildren5(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        
        res = self.aco.ListChildren(0,2,['*'])
        self.assertEqual(len(res),2)
        self.assertEqual(res[0]['DisplayName'],'rock')
        self.assertEqual(res[1]['DisplayName'],'pop')
        

    def test_ListChildren6(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        
        res=self.aco.ListChildren(0,2,['DisplayName', 'Type'])
        self.assertEqual(len(res),2)
        self.assertEqual(len(res[0]),2)
        self.assertEqual(len(res[1]),2)
        self.assertEqual(res[0]['DisplayName'],'rock')
        self.assertEqual(res[1]['DisplayName'],'pop')

    def test_ListItems1(self):
        item.Item._connect_to_dbus = mock.Mock()
        m=create_item_mock()
        self.aco._children.append(item.Item(self.parent, m))
        expect={'MIMEType': 'mp3',
                'DisplayName': 'mock',
                'Parent': '/mock/ed/path',
                'Type': 'audio'}
        self.assertEqual(len(self.aco.ListItems(0, 0, ['*'])), 1)
        res=self.aco.ListItems(0, 0, ['*'])
        self.assertTrue(self.smart_compare(res[0], expect))

    def test_ListItems2(self):
        item.Item._connect_to_dbus = mock.Mock()
        m=create_item_mock()
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(create_playlist_mock())
        expect={'MIMEType': 'mp3',
                'DisplayName': 'mock',
                'Parent': '/mock/ed/path',
                'Type': 'audio'}
        self.assertEqual(len(self.aco.ListItems(0, 0, ['*'])), 2)
        res=self.aco.ListItems(0, 0, ['*'])
        self.assertTrue(self.smart_compare(res[0], expect))
        self.assertTrue(self.smart_compare(res[1], expect))

    def test_ListItems3(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(create_playlist_mock())
        self.aco._children.append(create_playlist_mock())
        
        res=self.aco.ListItems(1, 2, ['*'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['DisplayName'], 'pop')
        self.assertEqual(res[1]['DisplayName'], 'metal')

    def test_ListItems4(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(create_playlist_mock())
        self.aco._children.append(create_playlist_mock())
        
        res=self.aco.ListItems(2, 5, ['*'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['DisplayName'], 'metal')
        self.assertEqual(res[1]['DisplayName'], 'techno')
    
    def test_ListItems5(self):
        item.Item._connect_to_dbus = mock.Mock()
        m = create_item_mock_named('rock')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('pop')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(create_playlist_mock())
        self.aco._children.append(create_playlist_mock())
        
        res=self.aco.ListItems(2, 5, ['DisplayName', 'Type'])
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 2)
        self.assertEqual(len(res[1]), 2)
        self.assertEqual(res[0]['DisplayName'], 'metal')
        self.assertEqual(res[0]['Type'], 'audio')
        self.assertEqual(res[1]['DisplayName'], 'techno')
        self.assertEqual(res[1]['Type'], 'audio')



    def testListContainers1(self):
        item.Item._connect_to_dbus = mock.Mock()
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        m = create_item_mock_named('metal')
        self.aco._children.append(item.Item(self.parent, m))
        m = create_item_mock_named('techno')
        self.aco._children.append(item.Item(self.parent, m))
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        self.aco._children.append(abstractcontainer.AbstractContainer(self.parent))
        res=self.aco.ListContainers(0, 2, ['*'])
        self.assertEqual(len(res), 2)
        res=self.aco.ListContainers(2, 2, ['*'])
        self.assertEqual(len(res), 2)
        res=self.aco.ListContainers(1, 5, ['*'])
        self.assertEqual(len(res), 3)


    def smart_compare(self, res, expect):
        for key in res:
            if (key == 'URLs') or (key == 'Path'):
                continue
            else:
                if res[key] != expect[key]:
                    return False
        return True

