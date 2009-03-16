from django.conf.urls.defaults import *
from django.conf import settings
from skel.categories.models import Category

category_dict = {
    'queryset': Category.objects.all(),
    'slug_field': 'slug',
}


urlpatterns = patterns('django.views.generic.list_detail',
    url(
        r'^(?P<slug>[^/]+)/$', 
        'object_detail', 
        category_dict,
        name='category-detail'
    ),
)

core_urlpatterns = patterns('',
    url(r'^category/', include(urlpatterns)),
)