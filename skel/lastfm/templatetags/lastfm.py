from django.conf import settings
from django import template
from time import mktime, localtime
from datetime import datetime
import feedparser

register = template.Library()

@register.inclusion_tag('lastfm/recent_tracks.html')
def show_recent_tracks(lastfm_user):
    d = feedparser.parse("http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.rss" % lastfm_user)
    tracks = d.entries[:15]
    for track in tracks:
        track.updated = datetime.fromtimestamp(mktime(track.updated_parsed))
        (track.artist, track.title) = track.title.split(u' \u2013 ', 1)
    return {'tracks': tracks}
