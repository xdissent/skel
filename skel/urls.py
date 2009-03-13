from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from skel.blog.feeds import EntryFeed, EntryCategoryFeed, EntryTagFeed
from skel.blog.models import Entry


admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('skel.core.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/(.*)', admin.site.root),
)