from __future__ import unicode_literals
import mock
import random
import base64


BUS_NAME = 'org.gnome.UPnP.MediaServer2.mopidy'
ROOT_PATH = '/org/gnome/UPnP/MediaServer2/mopidy'
CONT_IFACE = 'org.gnome.UPnP.MediaContainer2'
ITEM_IFACE ='org.gnome.UPnP.MediaItem2'
OBJ_IFACE = 'org.gnome.UPnP.MediaObject2'


def enc_id(uri):
    return base64.b32encode(uri).replace('=','_')

def create_track_mock():
    tr=mock.Mock()
    tr.uri=str(random.random()*100000)
    tr.name=str('Name'+str(random.random()*100000))
    return tr

def create_track_mock_named(name, uri):
    tr=mock.Mock()
    tr.name=name
    tr.uri=uri
    return tr
    
def create_playlist_mock():
    pl=mock.Mock()
    pl.uri=str(random.random()*100000)
    pl.name=str('Name'+str(random.random()*100000))
    pl.tracks=[]
    return pl
    
def creat_playlist_mock_named(uri, name):
    pl=mock.Mock()
    pl.uri=uri
    pl.name=name
    pl.tracks=[]
    return pl

def create_playlist_child_mock():
    pl=mock.Mock()
    pl._uri=str(random.random()*100000)
    pl._id=enc_id(pl._uri)
    pl._name=str('Name'+str(random.random()*100000))
    pl._tracks=[]
    return pl
    
def create_parent_mock():
    p=mock.Mock()
    p._path='/mock/ed/path'
    return p

def create_parent_mock_named(path):
    p=mock.Mock()
    p._path=path
    return p

def create_item_mock():
    i=mock.Mock()
    i.name='mock'
    i.uri=str(random.random()*100000)
    return i

def create_item_mock_named(name):
    i=mock.Mock()
    i.name=name
    i.uri=str(random.random()*100000)
    return i