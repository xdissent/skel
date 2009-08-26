from django.conf.urls.defaults import *

# Register default global URLs.
core_urlpatterns = patterns('',
    (r'^comments/', include('django.contrib.comments.urls')),
)