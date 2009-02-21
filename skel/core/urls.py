from django.conf.urls.defaults import *
from django.conf import settings
from tagging.models import Tag
from skel.core.views import tag_detail


tag_dict = {
    'queryset': Tag.objects.all(),
}


urlpatterns = patterns('',
    url(
        r'^tag/(?P<tag>[^/]+)/$', 
        tag_detail,
        tag_dict,
        name='tag-detail'
    ),
)