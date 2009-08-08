import sys
from django.conf.urls.defaults import *
from skel.core import settings


urlpatterns = []


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