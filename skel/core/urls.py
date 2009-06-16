import sys
from django.contrib import admin
from django.conf.urls.defaults import *
from skel.core import settings


admin.autodiscover()


urlpatterns = patterns('skel.core.views',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^admin/doc/$',
        'doc_index',
        {},
        name='django-admindocs-docroot',
    ),
    
    url(r'^admin/doc/skel/$',
        'doc_skel',
        {},
        name='skel-docroot',
    ),
)

if settings.CORE_USE_TAGS:
    from tagging.models import Tag
    
    urlpatterns += patterns('skel.core.views',
        url(r'^tag/(?P<tag>[^/]+)/$', 
            'tag_detail',
            {'queryset': Tag.objects.all()},
            name='tag-detail',
        ),
    )

if settings.CORE_SERVE_MEDIA:
    urlpatterns += patterns('skel.core.views',
        url(r'^static/(?P<path>.*)$',
        'static_server',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )


if settings.CORE_USE_REGISTRATION:
    urlpatterns += patterns('',
        (r'^accounts/', include('registration.urls')),
    )
    

# Import any core_urlpatterns Skel apps define
for app_name in settings.INSTALLED_APPS:
    if not app_name.startswith('skel.'):
        continue
    urls_module_name = '.'.join([app_name, 'urls'])
    try:
        mod = __import__(urls_module_name)
    except ImportError:
        continue
    try:
        urls_module = sys.modules[urls_module_name]
        urlpatterns += urls_module.core_urlpatterns
    except AttributeError:
        continue