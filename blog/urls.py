from django.conf.urls.defaults import *
from django.conf import settings
from blog.models import Entry

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'published',
}

tag_dict = {
    'queryset_or_model': info_dict['queryset'],
    'template_name': 'blog/entry_tag.html',
}

urlpatterns = patterns('django.views.generic.date_based',
    url(
        r'^/?$',
        'archive_index',
        info_dict,
        name='blog-latest'
    ),

    url(r'^(?P<year>\d{4})/$',
        'archive_year',
        info_dict,
        name='blog-year'
    ),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        'archive_month',
        info_dict,
        name='blog-month'
    ),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$',
        'archive_day',
        info_dict,
        name='blog-day'
    ),

    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'object_detail',
        dict(info_dict, slug_field='slug'),
        name='blog-detail'
    ),
)

urlpatterns += patterns('tagging.views',
    url(r'^tag/(?P<tag>[^/]+)/$',
        'tagged_object_list',
        tag_dict,
        name='blog-tag-detail'
    ),
)
