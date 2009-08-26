from django.conf import settings

SKEL_CORE_MARKUP_FLATPAGES = ('django.contrib.flatpages' in settings.INSTALLED_APPS)

SKEL_CORE_SERVE_ADMIN = ('django.contrib.admin' in settings.INSTALLED_APPS)

SKEL_CORE_TAGGING_ENABLED = ('tagging' in settings.INSTALLED_APPS)

SKEL_CORE_SERVE_MEDIA = False

SKEL_CORE_AJAXABLE_SUFFIX = '_xhr'

SKEL_CORE_SERVE_SITEMAP = ('django.contrib.sitemaps' in settings.INSTALLED_APPS)

SKEL_CORE_DEBUG_TOOLBAR_ENABLED = ('debug_toolbar' in settings.INSTALLED_APPS)

SKEL_CORE_HANDLER_500 = 'skel.core.views.server_error'


CORE_USE_REGISTRATION = ('registration' in settings.INSTALLED_APPS)