# Django settings for this project.
#
# Note: Avoid DEBUG dependent logic; Override local_settings instead.

import os


# Project settings
PROJ_LONG_NAME = 'Hartzog Skel'
PROJ_DESCRIPTION = 'The Hartzog Creative Django Framework'
PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_NAME = os.path.basename(os.path.dirname(__file__))


# Site settings
TIME_ZONE = 'America/Chicago'
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
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJ_PATH, 'sqlite.db')
VIRTUAL_ENVIRONMENT_PATH = os.path.expanduser('~/%s' % PROJ_NAME)
DEBUG = False
TEMPLATE_DEBUG = DEBUG
LANGUAGE_CODE = 'en-us'
USE_I18N = False
MEDIA_ROOT = os.path.join(PROJ_PATH, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
ROOT_URLCONF = PROJ_NAME + '.urls'
COMMENTS_APP = 'skel.comments'
CACHE_BACKEND = 'locmem:///?timeout=30&max_entries=200'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = PROJ_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
AUTH_PROFILE_MODULE = 'accounts.userprofile'
ACCOUNT_ACTIVATION_DAYS = 5
LOGIN_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = 'webmaster@example.com'
AKISMET_API_KEY = '652d0f8b1fcf'
FORCE_LOWERCASE_TAGS = True

GENERIC_CONTENT_LOOKUP_KWARGS = {
    'blog.entry': { 'public__exact': True },
    'massmedia.image': { 'public__exact': True },
    'massmedia.video': { 'public__exact': True },
    'massmedia.audio': { 'public__exact': True },
    'massmedia.flash': { 'public__exact': True },
    'massmedia.collection': { 'public__exact': True }
}

TEMPLATE_DIRS = [
    os.path.join(PROJ_PATH, 'templates'),
]

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
#     'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'massmedia',
    'profiles',
    'registration',
    'south',
    'tagging',
    'template_utils',
    'treemenus',
    'skel.accounts',
    'skel.blog',
    'skel.categories',
    'skel.comments',
    'skel.core',
    'skel.markup',
    'skel.quotes',
]


# Skel application settings
SKEL_BLOG_FEED_TITLE = ' '.join([PROJ_LONG_NAME, 'Blog Feed'])
SKEL_BLOG_FEED_DESCRIPTION = PROJ_DESCRIPTION
SKEL_CORE_SERVE_MEDIA = True


# MediaTemple specific settings overrides
if 'MT_ID' in os.environ:
    MT_ID = os.environ['MT_ID']
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'db%s_%s' % (MT_ID, PROJ_NAME)
    DATABASE_USER = 'db%s' % MT_ID
    DATABASE_PASSWORD = 'kKZ5Dv7g'
    DATABASE_HOST = 'internal-db.s%s.gridserver.com' % MT_ID
    VIRTUAL_ENVIRONMENT_PATH = '/home/%s/containers/django/mt_virtualenvs/%s' % (MT_ID, PROJ_NAME)
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
    FORCE_SCRIPT_NAME = ''
    SKEL_CORE_SERVE_MEDIA = False


#leave at end of file
try:
    from local_settings import *
except ImportError:
    pass