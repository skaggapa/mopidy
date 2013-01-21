from __future__ import unicode_literals

import logging
from ubuntu_sso.utils.txsecrets import ITEM_IFACE

try:
    import dbus
    import dbus.mainloop.glib
    import dbus.service
    import gobject
except ImportError as import_error:
    from mopidy.exceptions import OptionalDependencyError
    raise OptionalDependencyError(import_error)

from mopidy.frontends.ms2.defines import *
from mopidy.frontends.ms2.abstractitem import AbstractItem

logger = logging.getLogger('mopidy.frontends.ms2.item')

class Item(AbstractItem):
    """ The most basic item. Propably not usable
    
    """

    def __init__(self, parent, item):
        super(Item, self).__init__(parent, item)
        self._bus_name = self._connect_to_dbus()
        dbus.service.Object.__init__(self, self._bus_name, self._path)


class SpotifyItem(AbstractItem):
    """ An item for spotify tracks. Should be extended
    for more meta-data
    
    """
    # TODO write tests...
    
    def __init__(self, parent, item):
        super(SpotifyItem, self).__init__(parent, item)
        # TODO tests for thisframes
        # Override and add some properties.
#        self._props[ITEM_IFACE]['Bitrate'] = 176400
        self._props[ITEM_IFACE]['BitsPerSample'] = 16
        self._props[ITEM_IFACE]['SampleRate'] = 44100
        self._props[ITEM_IFACE]['Album'] = item.album.name
#        self._props[ITEM_IFACE]['Artist'] = item.artist[0] # TODO handle this better
        self._props[ITEM_IFACE]['MIMEType'] = 'audio/L16;rate=44100;channels=2'
        self._props[ITEM_IFACE]['DLNAProfile'] = 'LPCM' 
        self._props[ITEM_IFACE]['URLs'] = ['http://@ADDRESS@:51888/spotify/' 
                                           + item.uri]
        self._props[ITEM_IFACE]['TrackNumber'] = item.track_no
        self._bus_name = self._connect_to_dbus()
        try:
            dbus.service.Object.__init__(self, self._bus_name, self._path)
        except:
            self._remove_me = True
            
