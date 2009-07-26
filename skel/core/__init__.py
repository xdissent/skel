def handle_settings():
    from django.conf import settings as project_settings
    from skel.core.conf import autodiscover, configure_app
    
    
    if getattr(project_settings, 'CORE_AUTO_APP_SETTINGS', True):
        autodiscover()
    else:
        from skel.core import settings as core_settings
        configure_app(core_settings)
    
    from skel.core import settings
        
    # Extend django.contrib.flatpages.models.flatpage
    def markup_flatpages(sender, **kwargs):
        from skel.markupeditor.fields import add_extra_fields
    
        if sender._meta.module_name == 'flatpage':
            from django.db import models
            for f in sender._meta.fields:
                if f.name == 'content':
                    add_extra_fields(f, sender, f.name)
                                    
    if settings.CORE_MARKUP_FLATPAGES:
        from django.db.models.signals import class_prepared
        class_prepared.connect(markup_flatpages)

try:
    # Handle application settings
    handle_settings()
except ImportError:
    pass

