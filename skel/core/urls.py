import sys
from django.conf.urls.defaults import *
from skel.core import settings

urlpatterns = []
sitemaps = {}

# Import any core_urlpatterns and core_sitemaps Skel apps define.
for app_name in settings.INSTALLED_APPS:
    if not app_name.startswith('skel.'):
        continue
    urls_module_name = '.'.join([app_name, 'urls'])
    try:
        mod = __import__(urls_module_name)
    except ImportError:
        continue
    urls_module = sys.modules[urls_module_name]
    if hasattr(urls_module, 'core_urlpatterns'):
        urlpatterns += urls_module.core_urlpatterns
    if hasattr(urls_module, 'core_sitemaps'):
        sitemaps.update(urls_module.core_sitemaps)


if settings.SKEL_CORE_SERVE_MEDIA:
    urlpatterns += patterns('django.views.static',
        url(r'^static/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )


if settings.SKEL_CORE_SERVE_ADMIN:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        url('^admin/', include(admin.site.urls)),
    )


if settings.SKEL_CORE_TAGGING_ENABLED:
    tag_dict = {
        'template_name': 'core/tag.html',
        'allow_empty': True,
    }
    urlpatterns += patterns('tagging.views',
        url(r'^tag/(?P<tag>[^/]+)/$', 'tagged_object_list', tag_dict,
            name='tag'),
    )


if settings.SKEL_CORE_SERVE_SITEMAP:
    urlpatterns += patterns('django.contrib.sitemaps.views',
        url(r'^sitemap.xml$', 'sitemap', {'sitemaps': sitemaps}, name='sitemap')
    )


#if settings.SKEL_CORE_DEBUG_TOOLBAR_ENABLED:
    # from debug_toolbar.urls import urlpatterns as debug_toolbar_urls
    # This breaks right now:
    # urlpatterns += debug_toolbar_urls


handler500 = settings.SKEL_CORE_HANDLER_500