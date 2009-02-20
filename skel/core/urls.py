from django.conf.urls.defaults import *
from django.conf import settings
from tagging.models import Tag
from skel.core.models import Category
from skel.core.views import tag_detail

category_dict = {
    'queryset': Category.objects.all(),
}

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
    url(
        r'^category/(?P<slug>[^/]+)/$', 
        'django.views.generic.list_detail.object_detail', 
        category_dict,
        name='category-detail'
    ),
)