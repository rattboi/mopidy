from __future__ import unicode_literals

import logging

import pykka

from mopidy import settings
from mopidy.backends import base

logger = logging.getLogger('mopidy.backends.subsonic')

class SubsonicBackend(pykka.ThreadingActor, base.Backend):
    # Imports inside methods are to prevent loading of __init__.py to fail on
    # missing spotify dependencies.

    def __init__(self, audio):
        super(SubsonicBackend, self).__init__()

        from .library import SubsonicLibraryProvider
        #from .playback import SubsonicPlaybackProvider
        #from .session_manager import SubsonicSessionManager
        #from .playlists import SubsonicPlaylistsProvider

        self.library = SubsonicLibraryProvider(backend=self)
        #self.playback = SubsonicPlaybackProvider(audio=audio, backend=self)
        #self.playlists = SubsonicPlaylistsProvider(backend=self)

        self.uri_schemes = ['subsonic']

        # Fail early if settings are not present
        username = settings.SUBSONIC_USERNAME
        password = settings.SUBSONIC_PASSWORD

    def on_start(self):
        logger.info('Starting Subsonic Backend')

    def on_stop(self):
        logger.info('Exiting Subsonic Backend')
