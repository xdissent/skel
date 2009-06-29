from django.conf.urls.defaults import *
from skel.blog.models import Entry
from skel.blog import settings, feeds


entry_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'published',
}

tag_dict = {
    'queryset_or_model': entry_dict['queryset'],
    'template_name': 'blog/entry_tag_detail.html',
    'allow_empty': True,
}

category_dict = {
    'queryset': entry_dict['queryset'],
    'template_name': 'blog/entry_category_detail.html',
    'allow_empty': True,
    'paginate_by': 2,
}


urlpatterns = patterns('django.views.generic.date_based',
    url(
        r'^/?$',
        'archive_index',
        entry_dict,
        name='blog-entry-latest'
    ),

    url(r'^(?P<year>\d{4})/$',
        'archive_year',
        dict(entry_dict, make_object_list=True, allow_empty=True),
        name='blog-entry-year'
    ),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        'archive_month',
        dict(entry_dict, allow_empty=True),
        name='blog-entry-month'
    ),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
        'archive_day',
        dict(entry_dict, allow_empty=True),
        name='blog-entry-day'
    ),

    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'object_detail',
        dict(entry_dict, slug_field='slug'),
        name='blog-entry-detail'
    ),
)


blog_feeds = {
    'blog': feeds.EntryFeed,
}
blog_other_feeds = {}


if settings.BLOG_TAGS_ENABLED:
    urlpatterns += patterns('tagging.views',
        url(r'^tag/(?P<tag>[^/]+)/$',
            'tagged_object_list',
            tag_dict,
            name='blog-entry-tag-detail'
        ),
    )
    blog_other_feeds['tag'] = feeds.EntryTagFeed


if settings.BLOG_CATEGORIES_ENABLED:    
    urlpatterns += patterns('skel.categories.views',
        url(r'^category/(?P<slug>[^/]+)/$',
            'category_object_list',
            category_dict,
            name='blog-entry-category-detail'
        ),
    )
    blog_other_feeds['category'] = feeds.EntryCategoryFeed
    

core_urlpatterns = patterns('',
    url(r'^blog/', include(urlpatterns)),
)


if settings.BLOG_FEEDS_ENABLED:
    core_urlpatterns += patterns('',
        url(r'^feeds/blog/(?P<url>.*)/$',
            'django.contrib.syndication.views.feed', 
            {'feed_dict': blog_other_feeds}
        ),
        url(r'^feeds/(?P<url>.*)/$',
            'django.contrib.syndication.views.feed',
            {'feed_dict': blog_feeds},
            name='feed-root'),
    )