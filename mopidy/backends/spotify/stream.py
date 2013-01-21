from __future__ import unicode_literals

import logging

import pykka
import socket
import time

from spotify import Link, SpotifyError

from mopidy import settings
from mopidy.backends import base
from threading import Thread

logger = logging.getLogger('mopidy.backends.spotify.SpotifyStream')


class SpotifyStream(object):
    def __init__(self, spotify):
        logger.debug('__init__ called')
        self._quit = False
        self._cl_sock = None
        self._sock = None
        self._spotify = spotify

    def start(self):
        logger.debug("on_start")
        self._t = Thread(target = self.main_loop)
        self._t.start()
    
    def stop(self):
        logger.debug("on_stop")
        self._quit = True
        if self._cl_sock:
            self._cl_sock.close()
            self._cl_sock = None
        if self._sock:
            self._sock.close()
            self._sock = None

    def parse_request(self, msg):
        msg = msg.split(b'\0x0D\0x0A')[0].split(' ')[1].split('/')
        # first element in msg will be an empty string
        # msg[1] should be spotify
        # and msg[2] should be the spotify uri
        return msg[1], msg[2]
    
    def handle_request(self, sock, addr):
        logger.debug("parsing new request")
        self._cl_sock = sock
        data = self._cl_sock.recv(1024)
        service, uri = self.parse_request(data)
        logger.debug("got uri %s", uri)
        self._spotify.set_streaming(True, self.end_of_track_cb, 
                                    self.music_delivery_cb)
        link = Link.from_string(uri).as_track()
        self._spotify.session.load(link)
        duration = link.duration()
        self._write_header_ok(duration)
        self._spotify.session.play(1)


    def main_loop(self):
        logger.debug('stream main_loop started')
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((socket.gethostname(), 51888))
        self._sock.listen(1)
        self._sock.settimeout(4)
        while not self._quit:
            try:
                cl_sock, addr = self._sock.accept()
                if self._spotify.streaming:
                    self._spotify.session.unload()
                    time.sleep(0.2) # small sleep for now
                self.handle_request(cl_sock, addr)
            except socket.timeout:
                pass
            except Exception as e:
                logger.debug(e)
        logger.debug('exiting main_loop')
        self._sock = None


        
    def music_delivery_cb(self, frames, num_frames):
        logger.debug('m_d_cb')
        try:
            ret = self._cl_sock.send(frames)
            return int(ret/4)
        except:
            logger.debug('md Exception')
            return 0
        
    def end_of_track_cb(self):
        logger.debug("end of track cb")
        self._spotify.set_streaming(False, None, None)

    def _write_header_ok(self, duration):
        head = 'HTTP/1.1 200 OK\x0D\x0A'
        head += 'Date: '
        head += time.strftime('%a, %d %b %Y %H:%M:%S GMT' , time.gmtime())
        head += '\x0D\x0A'
        if duration :
            tmp = str((duration/1000 + 1) * 44100 * 4)
            head += 'Content-Length: '
            head += tmp
            head += '\x0D\x0A'
        head += 'Content-Type: audio/B16; rate=44100; channels=2\x0D\x0A'
        head +='\x0D\x0A'
        self._cl_sock.send(head)

    def _write_header_503(self):
        head = b'HTTP/1.1 503 Service Unavailable\x0D\x0A'
        head += '\x0D\x0A'
        self._cl_sock.send(head)

