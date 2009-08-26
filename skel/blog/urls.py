from django.conf.urls.defaults import *
from skel.core.sitemaps import GenericSitemap
from skel.generic.views import GenericView, ArchiveView, YearView, MonthView, DayView, DetailView
from skel.generic import GenericSuite
from skel.blog.models import Entry
from skel.blog import settings, feeds

# Create a suite for all entries.
urlpatterns = GenericSuite(Entry.objects.all()).urls


# Create entry date based URLs.
entry_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'published',
}


# Create core sitemaps.
core_sitemaps = {
    'blog': GenericSitemap(entry_dict, priority=0.6),
}


# Create syndication feeds.
blog_feeds = {'': feeds.EntryFeed}


# Create tagging URLs.
if settings.SKEL_BLOG_TAGGING_ENABLED:
    tag_dict = {
        'queryset_or_model': entry_dict['queryset'],
        'template_name': 'blog/tag.html',
        'allow_empty': True,
    }
    urlpatterns += patterns('tagging.views',
        url(r'^tag/(?P<tag>[^/]+)/$', 'tagged_object_list', tag_dict,
            name='tag'),
    )
    blog_feeds['tag'] = feeds.EntryTagFeed


# Create entry category URLs.
if settings.SKEL_BLOG_CATEGORIES_ENABLED:    
    category_dict = {
        'queryset': entry_dict['queryset'],
        'template_name': 'blog/category.html',
        'allow_empty': True,
        'paginate_by': 2,
    }
    urlpatterns += patterns('skel.categories.views',
        url(r'^category/(?P<slug>[^/]+)/$', 'category_object_list',
            category_dict, name='category'),
    )
    blog_feeds['category'] = feeds.EntryCategoryFeed


# Create feeds URLs.
if settings.SKEL_BLOG_FEEDS_ENABLED:
    urlpatterns += patterns('django.contrib.syndication.views',
        url(r'^feed/$', 'feed', {'url': '', 'feed_dict': blog_feeds}, name='feed'),
        url(r'^feed/(?P<url>.*)/$', 'feed', {'feed_dict': blog_feeds}),
    )


# Register default global URLs.
core_urlpatterns = patterns('',
    url(r'^blog/', include((urlpatterns, 'blog', 'blog'))),
)