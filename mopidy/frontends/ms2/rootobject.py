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
from mopidy.frontends.ms2.playlist import PlayList
from mopidy.frontends.ms2.abstractcontainer import AbstractContainer

logger = logging.getLogger('mopidy.frontends.ms2.rootobject')

# Must be done before dbus.SessionBus() is called
gobject.threads_init()
dbus.mainloop.glib.threads_init()


class MediaServer2RootObject(AbstractContainer):
    """ Root object for the Dbus interface. Implements
    MediaContainer2 as per the spec. Creates children
    and such stuff.
    """

#    properties = {'kalle': 1 }

    def __init__(self, core):
        self._path = ROOT_PATH
        super(MediaServer2RootObject,self).__init__(self)
        self._core = core
        self._props[OBJ_IFACE]['DisplayName']='mopidy'
        self._props[OBJ_IFACE]['Path'] = self._path
        
        self._bus_name = self._connect_to_dbus()
        dbus.service.Object.__init__(self,self._bus_name, self._path)
        for pl in self._core.playlists.playlists.get():
            self._children.append(PlayList(self, pl))
        if len(self._children) > 0:
            self.Updated()
    
    def playlists_loaded(self):
        logger.debug('playlists_loaded')
        logger.debug('num playlists %s', str(len(self._core.playlists.playlists.get())))
        # playlists are only refreshed or new
        # no changed properties
        for pl in self._core.playlists.playlists.get():
            if not self._check_for_pl(pl):
                self._children.append(PlayList(self, pl))
                self.Updated()
 
    def _check_for_pl(self, pl):
        """ Returns if the pl already exist among the children
            playlists have unique ids.
        """
        for c in self._children:
            if self._encode_id(pl.uri) == c._id:
                return True
        return False

    def playlists_updated(self, pl):
        for c in self._children:
            if self._encode_id(pl.uri) == c._id:
                c._updated(pl)
                return

