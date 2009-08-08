from django.conf import settings

CORE_MARKUP_FLATPAGES = ('django.contrib.flatpages' in settings.INSTALLED_APPS)

SKEL_CORE_SERVE_ADMIN = ('django.contrib.admin' in settings.INSTALLED_APPS)

CORE_USE_TAGS = ('tagging' in settings.INSTALLED_APPS)

CORE_SERVE_MEDIA = settings.DEBUG

CORE_AJAXABLE_TEMPLATE_SUFFIX = '_xhr'

CORE_VALIDATE_RESPONSE = settings.DEBUG

CORE_VALIDATE_RESPONSE_OPTIONS = {
    'doctype': 'strict',
    'output_xhtml': True,
    'input_encoding': 'utf8',
}

CORE_USE_REGISTRATION = ('registration' in settings.INSTALLED_APPS)