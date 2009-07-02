from django import template
from time import mktime
from datetime import datetime
from django.core.cache import cache
from feedcache.cache import Cache
from feedcache.cachedjango import CacheDjango

register = template.Library()

@register.inclusion_tag('lastfm/recent_tracks.html')
def show_recent_tracks(lastfm_user):
    storage = CacheDjango(cache)
    fc = Cache(storage)
    d = fc.fetch("http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.rss" % lastfm_user)
    tracks = d.entries
    for track in tracks:
        track.updated = datetime.fromtimestamp(mktime(track.updated_parsed))
        (track.artist, track.title) = track.title.split(u' \u2013 ', 1)
    return {'tracks': tracks}