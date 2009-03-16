from django.conf.urls.defaults import *
from django.conf import settings

from skel.markupeditor.views import preview

urlpatterns = patterns('skel.markupeditor.views',
    url(r'^preview/(?P<markup>[a-z]+)/', 'preview'),
)

core_urlpatterns = patterns('',
    url(r'^markupeditor/', include(urlpatterns)),
)