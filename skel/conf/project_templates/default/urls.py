from django.conf.urls.defaults import *
from django.contrib import admin
from skel.core.urls import urlpatterns

admin.autodiscover()
urlpatterns += patterns('',
    ('^admin/', include(admin.site.urls)),
)