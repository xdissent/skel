from django.conf.urls.defaults import *
from django.conf import settings

from skel.markup.views import preview

urlpatterns = patterns('skel.markup.views',
    url(r'^preview/(?P<markup>[a-z]+)/', 'preview'),
)

core_urlpatterns = patterns('',
    url(r'^markup/', include(urlpatterns)),
)