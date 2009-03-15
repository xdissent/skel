from django.conf.urls.defaults import *
from skel.core.urls import urlpatterns as core_patterns

urlpatterns = patterns('',
    url(r'', include(core_patterns)),
)