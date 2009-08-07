from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('skel.markup.views',
    url(r'^preview/(?P<engine_name>[a-z]+)/$', 'preview', name='preview'),
)

core_urlpatterns = patterns('',
    url(r'^markup/', include((urlpatterns, 'markup', 'markup'))),
)