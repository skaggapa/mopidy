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
from mopidy.frontends.ms2.abstractobject import AbstractObject
from mopidy.frontends.ms2.abstractitem import AbstractItem

logger = logging.getLogger('mopidy.frontends.ms2.playlistobject')

# Must be done before dbus.SessionBus() is called           
#gobject.threads_init()
#dbus.mainloop.glib.threads_init()

class AbstractContainer(AbstractObject):
    """ DBus object for playlists. Implements MediaContainer2
    spec.Abstract just to keep the common container functions
    and make filtering easier.
    
    """

    def __init__(self, parent):
        super(AbstractContainer, self).__init__(parent)
        self._children = []
        self._props[CONT_IFACE] = self._get_cont_iface_props()
        self._props[OBJ_IFACE]['Type'] = 'container'
                                                                        
    def _get_cont_iface_props(self):
        #TODO the counts
        return {
            'ChildCount': self._count_children,
            'ItemCount': self._count_items,
            'ContainerCount': self._count_containers,
            'Searchable': False
        }

    def _count_children(self):
        return len(self._children)

    def _count_items(self):
        count = 0
        for ch in self._children:
            if isinstance(ch, AbstractItem):
                count = count + 1
        return count

    def _count_containers(self):
        count = 0
        for ch in self._children:
            if isinstance(ch, AbstractContainer):
                count = count + 1
        return count

    
    def _updated(self, pl):
        #TODO fix should call Updated() when appropriate.
        return 0

    #MediaContainer signals                       
    @dbus.service.signal(dbus_interface=CONT_IFACE)
    def Updated(self):
        logger.debug('Updated called')

    @dbus.service.method(dbus_interface=CONT_IFACE,
                         in_signature='uuas', out_signature='aa{sv}')
    def ListChildren(self, offset, max , filt):
#        logger.debug('ListChildren called %i %i %s', offset, max, filt)
        result = []
        slice = self._slice_list(self._children, offset, max)
        for ch in slice:
            tmp = ch._query_props(filt)
            if len(tmp) > 0:
                result.append(tmp)
        return result


    @dbus.service.method(dbus_interface=CONT_IFACE,
                         in_signature='uuas', out_signature='aa{sv}')
    def ListItems(self, offset, max , filt):
#        logger.debug('ListItems called with %i %i %s', offset, max, filt)
        items = []
        result = []
        for child in self._children:
            if isinstance(child, AbstractItem):
                items.append(child)
        
        slice = self._slice_list(items, offset, max)
        for ch in slice:
            tmp = ch._query_props(filt)
            if len(tmp) > 0:
                result.append(tmp)
        return result

    @dbus.service.method(dbus_interface=CONT_IFACE,
                         in_signature='uuas', out_signature='aa{sv}')
    def ListContainers(self, offset, max , filt):
#        logger.debug('ListContainer Called with %i %i %s', offset, max, filt)
        containers = []
        result = []
        for child in self._children:
            if isinstance(child, AbstractContainer):
                containers.append(child)
        
        slice = self._slice_list(containers, offset, max)
        for ch in slice:
            tmp = ch._query_props(filt)
            if len(tmp) > 0:
                result.append(tmp)
        return result

    @dbus.service.method(dbus_interface=CONT_IFACE,
                         in_signature='suuas', out_signature='aa{sv}')
    def SearchObjects(self, query,offset,max,filt):
#        logger.debug('SeachObjects called with %s %i %i %s', query, offset, max, filt)
        # TODO not implemented.
        return []
