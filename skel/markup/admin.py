from django.contrib import admin
from skel.markup.forms import markedup_modelform_factory

class MarkedUpAdmin(admin.ModelAdmin):
    """A generic model admin class for models registered with markup.
    
    This class will automatically define an appropriate form class using
    the model which which it was registered. Note: the ``form`` attribute 
    of this class has no effect when overridden in a subclass.
    
    Example usage in ``skel/blog/admin.py``:
    
    from django.contrib import admin
    from skel.core.markup.admin import MarkedUpAdmin
    from skel.blog.models import Entry
    
    admin.site.register(Entry, MarkedUpAdmin)
    
    """
    def __init__(self, *args, **kwargs):
        """Initialize and create form for the model."""
        super(MarkedUpAdmin, self).__init__(*args, **kwargs)
        self.form = markedup_modelform_factory(self.model)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MarkedUpAdmin, self).formfield_for_dbfield(db_field, 
                                                                 **kwargs)
        # Add markup class name to appropriate fields.
        if db_field.name in self.form.markup_fields:
            old_class = field.widget.attrs['class']
            new_class = ' '.join([old_class, 'markup'])
            field.widget.attrs['class'] = new_class
        return field