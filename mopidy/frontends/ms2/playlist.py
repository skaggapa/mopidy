from __future__ import unicode_literals

import logging

try:
    import dbus
    import dbus.mainloop.glib
    import dbus.service
    import gobject
except ImportError as import_error:
    from mopidy.exceptions import OptionalDependencyError
    raise OptionalDependencyError(import_error)

from mopidy.frontends.ms2.defines import *
from mopidy.frontends.ms2.abstractcontainer import AbstractContainer
from mopidy.frontends.ms2.item import Item
from mopidy.frontends.ms2.item import SpotifyItem

logger = logging.getLogger('mopidy.frontends.ms2.playlistobject')

# Must be done before dbus.SessionBus() is called           
#gobject.threads_init()
#dbus.mainloop.glib.threads_init()

class PlayList(AbstractContainer):
    """ DBus object for playlists. Implements MediaContainer2
    spec.
    """

    def __init__(self, parent, pl):
        super(PlayList,self).__init__(parent)
        self._parent = parent
        self._pl = pl
        self._id = self._encode_id(self._pl.uri)
        self._path=self._parent._path+'/'+self._id
        self._props[OBJ_IFACE]['Path'] = self._path
        self._props[OBJ_IFACE]['DisplayName'] = self._pl.name
        self._bus_name = self._connect_to_dbus()
        dbus.service.Object.__init__(self, self._bus_name, self._path)

        for tr in self._pl.tracks:
            item_ = self.item_selector(tr)
            self._children.append(item_)
        if len(self._children) > 0:
            self.Updated()
            
            
    def item_selector(self, track):
        logger.debug(track.uri)
        tmp=track.uri.split(':')
        if len(tmp) > 1:
            if tmp[0] == 'spotify':
                return SpotifyItem(self, track)        
        return Item(self, track)
    
