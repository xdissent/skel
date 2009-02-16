# Django settings for this project.
#
# Note: Avoid DEBUG dependent logic; Override local_settings instead.

import os

PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_NAME = os.path.basename(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Greg Thornton', 'xdissent@gmail.com'),
    ('Phil Thornton', 'pixelkicker@gmail.com'),
)

INTERNAL_IPS = (
    '98.193.129.254',
    '98.193.195.124',
)

MANAGERS = ADMINS

# Necessary for (mt) Django GridContainer
FORCE_SCRIPT_NAME = ''

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'db36218_XXX'
DATABASE_USER = 'db36218'
DATABASE_PASSWORD = 'kKZ5Dv7g'
DATABASE_HOST = 'internal-db.s36218.gridserver.com'
DATABASE_PORT = ''

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
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'FcPpmwaBl4XdS5KLBj7NrLqpWiuV4NGa'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = PROJ_NAME + '.urls'

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJ_PATH, 'templates'),
]

try:
	from skel import __path__ as skel_path
	TEMPLATE_DIRS.append(os.path.join(skel_path[0], 'templates'))
except ImportError:
	pass

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
    'django.contrib.markup',
    'django.contrib.comments',
    'template_utils',
    'tagging',
    'profiles',
    #'skel.core',
    'skel.blog',
    'skel.accounts',
    'skel.portfolio',
    'skel.lastfm',
    'skel.markupeditor',
    'skel.superimage',
    'skel.quotes',
)

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

AUTH_PROFILE_MODULE = 'accounts.userprofile'

PORTFOLIO_PROJECT_THUMB_SIZE = (100, 100)

#leave at end of file
try:
    from local_settings import *
except ImportError:
    pass
