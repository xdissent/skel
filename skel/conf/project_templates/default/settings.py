# Django settings for this project.
#
# Note: Avoid DEBUG dependent logic; Override local_settings instead.

import os

PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_NAME = os.path.basename(os.path.dirname(__file__))

if 'MT_ID' in os.environ:
    MT_ID = os.environ['MT_ID']
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'db%s_%s' % (MT_ID, PROJ_NAME)
    DATABASE_USER = 'db%s' % MT_ID
    DATABASE_PASSWORD = 'kKZ5Dv7g'
    DATABASE_HOST = 'internal-db.s%s.gridserver.com' % MT_ID
    VIRTUAL_ENVIRONMENT_PATH = '/home/%s/containers/django/mt_virtualenvs/%s' % (MT_ID, PROJ_NAME)
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
else:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = os.path.join(PROJ_PATH, 'sqlite.db')
    VIRTUAL_ENVIRONMENT_PATH = os.path.expanduser('~/%s' % PROJ_NAME)
    CORE_SERVE_MEDIA = True
    CACHE_BACKEND = 'locmem:///?timeout=30&max_entries=200'


BLOG_FEED_TITLE = 'Hartzog Skel Blog Feed'
BLOG_FEED_DESCRIPTION = 'The Hartzog Creative Django Framework'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Greg Thornton', 'xdissent@gmail.com'),
    ('Phil Thornton', 'pixelkicker@gmail.com'),
)

INTERNAL_IPS = (
    '127.0.0.1',
)

MANAGERS = ADMINS

# Necessary for (mt) Django GridContainer
FORCE_SCRIPT_NAME = ''



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJ_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'FcPpmwaBl4XdS5KLBj7NrLqpWiuV4NGa'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = PROJ_NAME + '.urls'

TEMPLATE_DIRS = [
    os.path.join(PROJ_PATH, 'templates'),
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
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
    'skel.markupeditor',
    'skel.accounts',
    'skel.portfolio',
    'skel.lastfm',
    'skel.superimage',
    'skel.quotes',
)

COMMENTS_APP = 'skel.core'

CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = PROJ_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

AUTH_PROFILE_MODULE = 'accounts.userprofile'

FORCE_LOWERCASE_TAGS = True

RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'doctitle_xform': False,
    'initial_header_level': '2',
    'cloak_email_addresses': True,
}

GENERIC_CONTENT_LOOKUP_KWARGS = {
    'blog.post': { 'public__exact': True },
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