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
import base64

logger = logging.getLogger('mopidy.frontends.ms2.abstract')

class AbstractObject(dbus.service.Object):
    """ Base class for the mediacontainers/items
    Implicit inheritance from MediaItem2 (has no methods)
    All properties must be set in the class that inherits
    this class

    Implements DBus properties interface
    
    """
    def __init__(self, parent):
        self._parent = parent
        self._props = { OBJ_IFACE: self._get_obj_iface_props() }

    def _get_obj_iface_props(self):
        return {
            'Parent': self._parent._path,
        }

    def _connect_to_dbus(self):
        mainloop = dbus.mainloop.glib.DBusGMainLoop()
        bus_name = dbus.service.BusName(BUS_NAME, 
                                        dbus.SessionBus(mainloop=mainloop))
        logger.info('Connected to D-Bus %s', BUS_NAME)
        return bus_name

    def remove_from_connection(self):
        super(AbstractObject, self).remove_from_connection()


    def _query_props(self, filt):
        """ Used by parent objects to query its children
        for its respective properties."""   
        res={}
        for iface in self._props:
            for (key, getter) in self._props[iface].iteritems():
                if (filt == ['*']):
                     res[key] =  getter() if callable(getter) else getter
                else:
                    for st in filt:
                        if st == key:
                            res[key] = getter() if callable(getter) else getter
                            break
                            
        return res

    def _encode_id(self, uri):
        return base64.b32encode(uri).replace('=', '_')
    
    def _slice_list(self, list, offset, max):
        # First some input validation negative values should
        # be avoided.
        if offset < 0:
            offset = 0
        if max < 0:
            max = 0

        if max == 0:
            return list[offset:]
        else:
            if offset+max > len(list):
                return list[offset:]
            else:
                return list[offset:(offset+max)]

    ### Properties Interface
    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ss', out_signature='v')
    def Get(self, interface, prop):
#        logger.debug('%s.Get(%s, %s) called', dbus.PROPERTIES_IFACE, 
#                     repr(interface), repr(prop))
        getter = self._props[interface][prop]
        if callable(getter):
            return getter()
        else:
            return getter

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='s', out_signature='a{sv}',
                         )
    def GetAll(self, interface):
#        logger.debug('%s.GetAll(%s) called', dbus.PROPERTIES_IFACE, 
#                     repr(interface))
        getters = {}
        for key, getter in self._props[interface].iteritems():
            getters[key] = getter() if callable(getter) else getter
        return getters

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ssv', out_signature='')
    def Set(self, interface, prop, value):
        logger.debug('%s.Set(%s, %s, %s) called', interface, prop, value)
        # Cant set properties so the function does nothing.

    @dbus.service.signal(dbus_interface=dbus.PROPERTIES_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed_properties,
                          invalidated_properties):
        logger.debug('%s.PropertiesChanged(%s, %s, %s) signaled',
                     dbus.PROPERTIES_IFACE, interface, changed_properties,
                     invalidated_properties)
        # maybe implemented the client does not require it thou.


