import sys
import types
import logging
from django.conf import settings as project_settings
from skel.conf import settings as app_settings

# Global cache of apps whose settings have been handled.
_settled = None

class AppSettings(types.ModuleType):
    """Application level settings module class.
    
    Skel's application level settings are objects that replace the normal 
    settings module for an app. The ``AppSettings`` class provides a way
    for applications to use ``<app>/settings.py`` as a default value store,
    from which values are automatically overridden if present in a project's
    settings.
    
    """
    def __init__(self, module_name, default_settings):
        """Stores the app level defaults for an app settings module."""
        self.default_settings = default_settings
        super(AppSettings, self).__init__(module_name)
        
    def __getattr__(self, name):
        """Returns a value from the project setting or defaults if not found."""
        try:
            from django.conf import settings
            return getattr(settings, name)
        except AttributeError:
            return getattr(self.default_settings, name)

def configure_app(app_name, settings_module_name='settings'):
    """Applies project and app settings to an app's settings module."""
    settings_module_name = '.'.join([app_name, settings_module_name])
    logging.debug('Configuring settings for app "%s": %s' % (settings_module_name, app_name))
    __import__(app_name)
    app = sys.modules[app_name]
    mod = __import__(app_name, {}, {}, ['settings'])
    try:
        settings_module = sys.modules[settings_module_name]
    except KeyError:
        return
    settings = AppSettings(settings_module_name, settings_module)
    sys.modules[settings_module_name] = settings
    setattr(app, 'settings', settings)

def autodiscover():
    """Finds app-level settings and overrides them if appropriate.
    
    Generally called from ``handle_app_settings``, this function detects
    application level settings in all installed apps and overrides all
    values with those found in the project's settings module. If an app
    contains a settings module that should *not* be processed by Skel,
    it should be added to ``SKEL_CONF_IGNORE_APPS`` in the project's
    settings file or problems may arise. Known offenders are provided
    as a default in ``skel.conf.settings``. 
    
    """
    logging.debug('Autodiscovering application settings.')
    global _settled
    ignore_apps = getattr(app_settings, 
                          'SKEL_CONF_IGNORE_APPS', [])
    ignore_apps = getattr(project_settings, 
                          'SKEL_CONF_IGNORE_APPS', ignore_apps)
    for app_name in project_settings.INSTALLED_APPS:
        if app_name in ignore_apps or app_name in _settled:
            continue
        try:
            configure_app(app_name)
            _settled.append(app_name)
        except ImportError:
            logging.debug('Caught ImportError when configuring %s' % app_name)
            _settled.append(app_name)
            continue

def handle_app_settings():
    """Sets up Skel's application level settings.
    
    Skel allows applications to provide their own application specific
    settings in ``<app>/settings.py``, which can be overridden in the
    project settings. Ideally this should be called as soon as possible
    to ensure settings are configured before they're needed.
    
    This function is only effective once.
    
    """
    global _settled
    print "Handling app settings."
    if _settled is None:
        _settled = []
        auto_settings = getattr(app_settings, 
                                'SKEL_CONF_AUTO_APP_SETTINGS', True)
        auto_settings = getattr(project_settings, 
                                'SKEL_CONF_AUTO_APP_SETTINGS', auto_settings)
        if auto_settings:
            autodiscover()
        # Just in case skel.conf isn't in INSTALLED_APPS, configure it manually.
        configure_app('skel.conf')