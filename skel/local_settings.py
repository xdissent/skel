import os

PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_NAME = os.path.basename(os.path.dirname(__file__))

VIRTUAL_ENVIRONMENT_PATH = '/Users/xdissent/.virtualenvs/hartzog_skel'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJ_PATH, 'sqlite.db')

CACHE_BACKEND = 'locmem:///?timeout=30&max_entries=200'

CORE_SERVE_MEDIA = True