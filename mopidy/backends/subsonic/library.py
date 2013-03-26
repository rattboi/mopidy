from __future__ import unicode_literals

import logging

from mopidy import settings
from mopidy.backends import base
from mopidy.models import SearchResult

from .client import SubsonicRemoteClient

logger = logging.getLogger('mopidy.backends.subsonic')

class SubsonicLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(SubsonicLibraryProvider, self).__init__(*args, **kwargs)
        self.remote = SubsonicRemoteClient(settings.SUBSONIC_SERVER_URI, 
            settings.SUBSONIC_SERVER_PORT,
            settings.SUBSONIC_USERNAME, 
            settings.SUBSONIC_PASSWORD)

    def find_exact(self, **query):
        return self.search(**query)

    def search(self, **query):
        self._validate_query(query)
        if not query:
            # Fetch all data(browse library)
            return SearchResult(
                uri='subsonic:search',
                tracks=self.remote.get_tracks())

        for (field, val) in query.iteritems():
            if field == "album":
                return SearchResult(
                    uri='subsonic:search',
                    tracks=self.remote.get_album_by(val[0]) or [])
            elif field == "artist":
                return SearchResult(
                    uri='subsonic:search',
                    tracks=self.remote.get_item_by(val[0]) or [])
            elif field == "any":
                return SearchResult(
                    uri='subsonic:search',
                    tracks=self.remote.get_item_by(val[0]) or [])
            else:
                raise LookupError('Invalid lookup field: %s' % field)

        return []

    def lookup(self, uri):
        try:
            id = uri.split("//")[1]
            logger.debug(u'Subsonic track id for "%s": %s', id, uri)
            return [self.remote.get_track(id, True)]
        except Exception as error:
            logger.debug(u'Failed to lookup "%s": %s', uri, error)
            return []

    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
