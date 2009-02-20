from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    url(
        r'^tag/(?P<tag>[^/]+)/$', 
        'django.views.generic.simple.direct_to_template', 
        {
            'template': 'core/tag_detail.html'
        },
        name='tag-detail'
    ),
)