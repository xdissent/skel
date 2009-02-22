from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from skel.core.urls import urlpatterns as core_urls
from skel.blog.feeds import EntryFeed, EntryCategoryFeed, EntryTagFeed


blog_feeds = {
    'blog': EntryFeed,
}

blog_other_feeds = {
    'category': EntryCategoryFeed,
    'tag': EntryTagFeed,
}


admin.autodiscover()

urlpatterns = core_urls

urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/(.*)', admin.site.root),
    url(r'^blog/', include('skel.blog.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^portfolio/', include('skel.portfolio.urls')),
    url(r'^users/', include('skel.accounts.urls')),
    url(r'^markupeditor/', include('skel.markupeditor.urls')),
    url(r'^category/', include('skel.categories.urls')),
    
    # TODO: Delete these files    
    url(r'^markupeditordemo/$', 'django.views.generic.simple.direct_to_template', {'template': 'markupeditor.html'}),
    url(r'^superimage/$', 'django.views.generic.simple.direct_to_template', {'template': 'superimage.html'}),
    url(r'^splitpane/$', 'django.views.generic.simple.direct_to_template', {'template': 'splitpane.html'}),
    url(r'^crop/$', 'django.views.generic.simple.direct_to_template', {'template': 'crop.html'}),
    
    url(r'^feeds/blog/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_other_feeds}),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_feeds}),

)

# TODO: Change this to some other test
if settings.DEBUG:
    from django.views.static import serve
    from django.http import Http404, HttpResponseNotFound
    
    def static_server(*args, **kwargs):
        try:
            return serve(*args, **kwargs)
        except Http404:
            return HttpResponseNotFound('Not Found')
            

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', static_server,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
