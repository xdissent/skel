CORE_AUTO_APP_SETTINGS = True

CORE_AUTO_APP_SETTINGS_IGNORE_APPS = (
    'django.contrib.comments',
    'tagging',
)

# TODO: Fix these so they check INSTALLED_APPS
CORE_MARKUP_FLATPAGES = True
CORE_MARKUP_COMMENTS = True

CORE_SERVE_MEDIA = False

CORE_AJAXABLE_TEMPLATE_SUFFIX = '_xhr'

CORE_VALIDATE_RESPONSE = True

CORE_VALIDATE_RESPONSE_OPTIONS = {
    'doctype': 'strict',
    'output_xhtml': True,
    'input_encoding': 'utf8',
}