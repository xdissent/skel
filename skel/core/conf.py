import sys
import types
from django.conf import settings
from django.db.models.loading import get_app, get_apps
from skel.core.settings import CORE_AUTO_APP_SETTINGS_IGNORE_APPS

# TODO: Test

IGNORE_APPS = getattr(settings, 'CORE_AUTO_APP_SETTINGS_IGNORE_APPS',
    CORE_AUTO_APP_SETTINGS_IGNORE_APPS)


class AppSettings(types.ModuleType):
    def __init__(self, module_name, default_settings):
        self.default_settings = default_settings
        super(AppSettings, self).__init__(module_name)
        
    def __getattr__(self, name):
        try:
            return getattr(settings, name)
        except AttributeError:
            pass
        return getattr(self.default_settings, name)


def configure_app(app_name, settings_module_name='settings'):
    settings_module_name = '.'.join([app_name, settings_module_name])

    try:
        __import__(app_name)
    except ImportError:
        raise
    app = sys.modules[app_name]
    
    mod = __import__(app_name, {}, {}, ['settings'])
    try:
        settings_module = sys.modules[settings_module_name]
    except KeyError:
        raise ImportError

    settings = AppSettings(settings_module_name, settings_module)
    sys.modules[settings_module_name] = settings
    setattr(app, 'settings', settings)
    
        
def autodiscover():
    settled = []
    for app_name in settings.INSTALLED_APPS:
        if app_name in IGNORE_APPS or app_name in settled:
            continue
        try:
            configure_app(app_name)
        except ImportError:
            continue
        finally:
            settled.append(app_name)