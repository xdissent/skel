from django.conf.urls.defaults import *
from django.conf import settings
from skel.categories.models import Category

category_dict = {
    'queryset': Category.objects.all(),
    'slug_field': 'slug',
}


urlpatterns = patterns('',
    url(
        r'^(?P<slug>[^/]+)/$', 
        'django.views.generic.list_detail.object_detail', 
        category_dict,
        name='category-detail'
    ),
)