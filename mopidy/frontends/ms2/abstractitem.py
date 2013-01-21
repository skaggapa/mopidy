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
from mopidy.frontends.ms2.abstractobject import AbstractObject

class AbstractItem(AbstractObject):
    """ AbstractItem(AbstractObject)
    Implements the basic item interface without any extended
    properties.
    
    Subclasses can add extra properties.
    
    """

    def __init__(self, parent, item):
        # It adds some that actually belong in the Object
        # but the object cant know these things
        # and it was a simple solution.
        super(AbstractItem, self).__init__(parent)
        self._item = item
        self._remove_me = False
        self._id = self._encode_id(self._item.uri)
        self._path = self._parent._path + '/' + self._id
        self._props[OBJ_IFACE]['Path'] = self._path
        self._props[OBJ_IFACE]['DisplayName'] = self._item.name
        self._props[OBJ_IFACE]['Type'] = 'audio'
        self._props[ITEM_IFACE] = {}
        self._props[ITEM_IFACE]['URLs'] = [self._item.uri]
        self._props[ITEM_IFACE]['MIMEType'] = 'mp3'