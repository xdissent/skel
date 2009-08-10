# Django settings for this project.
#
# Note: Avoid DEBUG dependent logic; Override local_settings instead.

import os

PROJ_LONG_NAME = 'Hartzog Skel'
PROJ_DESCRIPTION = 'The Hartzog Creative Django Framework'
PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_NAME = os.path.basename(os.path.dirname(__file__))

SITE_ID = 1
ADMINS = (
    ('Greg Thornton', 'xdissent@gmail.com'),
    ('Phil Thornton', 'pixelkicker@gmail.com'),
)
INTERNAL_IPS = (
    '127.0.0.1',
)
MANAGERS = ADMINS
SECRET_KEY = 'FcPpmwaBl4XdS5KLBj7NrLqpWiuV4NGa'


if 'MT_ID' in os.environ:
    # MediaTemple specific settings.
    MT_ID = os.environ['MT_ID']
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'db%s_%s' % (MT_ID, PROJ_NAME)
    DATABASE_USER = 'db%s' % MT_ID
    DATABASE_PASSWORD = 'kKZ5Dv7g'
    DATABASE_HOST = 'internal-db.s%s.gridserver.com' % MT_ID
    VIRTUAL_ENVIRONMENT_PATH = '/home/%s/containers/django/mt_virtualenvs/%s' % (MT_ID, PROJ_NAME)
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
    FORCE_SCRIPT_NAME = ''
else:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = os.path.join(PROJ_PATH, 'sqlite.db')
    VIRTUAL_ENVIRONMENT_PATH = os.path.expanduser('~/%s' % PROJ_NAME)
    SKEL_CORE_SERVE_MEDIA = True
    CACHE_BACKEND = 'locmem:///?timeout=30&max_entries=200'

BLOG_FEED_TITLE = ' '.join([PROJ_LONG_NAME, 'Blog Feed'])
BLOG_FEED_DESCRIPTION = PROJ_DESCRIPTION

DEBUG = False

TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

USE_I18N = False

MEDIA_ROOT = os.path.join(PROJ_PATH, 'static')
MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware'
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'south',
    'template_utils',
    'tagging',
    'registration',
    'profiles',
    'massmedia',
    'treemenus',
    'debug_toolbar',
    'skel.core',
    'skel.blog',
    'skel.categories',
    'skel.markup',
    'skel.accounts',
#    'skel.portfolio',
#    'skel.lastfm',
#    'skel.superimage',
    'skel.quotes',
)

ROOT_URLCONF = PROJ_NAME + '.urls'

TEMPLATE_DIRS = [
    os.path.join(PROJ_PATH, 'templates'),
]

# COMMENTS_APP = 'skel.core'

CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = PROJ_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

AUTH_PROFILE_MODULE = 'accounts.userprofile'

FORCE_LOWERCASE_TAGS = True

GENERIC_CONTENT_LOOKUP_KWARGS = {
    'blog.entry': { 'public__exact': True },
    'massmedia.image': { 'public__exact': True },
    'massmedia.video': { 'public__exact': True },
    'massmedia.audio': { 'public__exact': True },
    'massmedia.flash': { 'public__exact': True },
    'massmedia.collection': { 'public__exact': True }
}

# TODO: Move these to accounts settings
ACCOUNT_ACTIVATION_DAYS = 5
LOGIN_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = 'webmaster@example.com'

AKISMET_API_KEY = '652d0f8b1fcf'

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.firebug.FirebugPanel',
    'debug_toolbar.panels.validator.ValidatorPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.profile.ProfileDebugPanel',
)

#leave at end of file
try:
    from local_settings import *
except ImportError:
    pass