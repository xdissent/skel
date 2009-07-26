from django.conf import settings

COMMENTS_MARKUP = ('django.contrib.comments' in settings.INSTALLED_APPS)

COMMENTS_ENABLED_DEFAULT = True