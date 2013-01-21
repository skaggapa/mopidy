from __future__ import unicode_literals

import logging

import pykka

from mopidy import settings
from mopidy.core import CoreListener
from mopidy.frontends.ms2.rootobject import MediaServer2RootObject

logger = logging.getLogger('mopidy.frontends.ms2.actor')

class MediaServer2Frontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, core):
        super(MediaServer2Frontend, self).__init__()
        self.core = core
        self.indicate_server = None
        self.ms2_object = None


    def on_start(self):
        print 'on start'
        try:
            self.ms2_object = MediaServer2RootObject(self.core)
        except Exception as e:
            logger.error('Mediaserver2 rootobject setup failed (%s)', e)
            self.stop()


    def on_stop(self):
        print 'on stop'
        logger.debug('Removing MediaServer2 object from D-Bus connection ...')
        if self.ms2_object:
            self.ms2_object.remove_from_connection()
            self.ms2_object = None
        logger.debug('MediaServer2Frontent Stopped')


    def playlists_loaded(self):
        logger.error('Recieved playlists_loaded event')
        if self.ms2_object:
            self.ms2_object.playlists_loaded()


    def playlist_changed(self, playlist):
        logger.error('Recieved playlist_changed event')
        if self.ms2_object:
            self.ms2_object.playlists_changed()
        #TODO implement signals..
