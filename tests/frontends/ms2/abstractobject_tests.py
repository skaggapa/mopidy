from __future__ import unicode_literals

import sys

import mock
import pykka

from mopidy import core, exceptions, settings
from mopidy.backends import dummy

import dbus
from ms2_tests_helpers import *
try:
    from mopidy.frontends.ms2 import abstractobject
except exceptions.OptionalDependencyError:
    pass

from tests import unittest

@unittest.skipUnless(sys.platform.startswith('linux'), 'requres linux')
class AbstractObjectTests(unittest.TestCase):
    """ Could be extended to more of the methods, not 100 % 
    coverage
    
    """
    def setUp(self):
        self.parent=create_parent_mock()
        self.ao=abstractobject.AbstractObject(self.parent)
   
    def test_constructor1(self):
        self.assertEqual(self.ao._parent, self.parent) 
    
    def test_properties(self):
        self.assertEqual(self.ao._props[OBJ_IFACE]['Parent'], 
                         self.parent._path)
        
    def test_query_props(self):
        self.ao._props[OBJ_IFACE]={'Test1': 'test11',
                                   'Test2': 'test12',
                                   'Test3': 1,
                                   'Test4': False}
        
        expect={}
        expect['Test1']= 'test11'
        expect['Test2']= 'test12'
        expect['Test3']= 1
        expect['Test4']= False                        
        self.assertEqual(self.ao._query_props(['*']),expect)  
        expect={}
        expect['Test1']= 'test11'
        expect['Test2']= 'test12'
        self.assertEqual(self.ao._query_props(['Test1',  'Test2']), expect)  
        
        expect={}
        expect['Test2']= 'test12'
        expect['Test3']= 1
        expect['Test4']= False                        
        self.assertEqual(self.ao._query_props(['Test2', 'Test3', 'Test4']), expect)

    def test_Get(self):
        self.assertEqual(self.ao.Get(OBJ_IFACE,'Parent'), self.parent._path)

    def test_GetAll(self):
        expect={}
        expect['Test1']= 'test11'
        expect['Test2']= 'test12'
        expect['Test3']= 1
        expect['Test4']= False                        
        self.ao._props[OBJ_IFACE]={}
        self.ao._props[OBJ_IFACE]['Test1']='test11'
        self.ao._props[OBJ_IFACE]['Test2']='test12'
        self.ao._props[OBJ_IFACE]['Test3']=1
        self.ao._props[OBJ_IFACE]['Test4']=False
        self.assertEqual(self.ao.GetAll(OBJ_IFACE), expect)

    def test_slice_list(self):
        obj=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEquals(self.ao._slice_list(obj, 5, 0), [6, 7, 8, 9, 10])
        self.assertEquals(self.ao._slice_list(obj, 4, 0), [5, 6, 7, 8, 9, 10])
        self.assertEquals(self.ao._slice_list(obj, 2, 5), [3, 4, 5, 6, 7])
        self.assertEquals(self.ao._slice_list(obj, 5, 5), [6, 7, 8, 9, 10])
        self.assertEquals(self.ao._slice_list(obj, 5, 10), [6, 7, 8, 9, 10])
        self.assertEquals(self.ao._slice_list(obj, 2, 2), [3, 4])
        self.assertEquals(self.ao._slice_list(obj, 0, 0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEquals(self.ao._slice_list(obj, 1, 0), [2, 3, 4, 5, 6, 7, 8, 9, 10])


