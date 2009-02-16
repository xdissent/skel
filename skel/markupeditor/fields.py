from django import forms
from django.db import models
from skel.markupeditor.markups import registry, get_choices

class MarkupEditorCreator(object):
    """
    Difficult.
    """
    def __init__(self, field):
        self.field = field
        self.markup_name = '%s_markup' % self.field.name
        self.rendered_name = '%s_rendered' % self.field.name

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')

        rendered = getattr(obj, self.rendered_name, None)
        
        #if rendered:
        #    return rendered
        
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
    
        markup = getattr(obj, self.markup_name, None)
        
        obj.__dict__[self.field.name] = self.field.to_python(value)

        if not markup:
            return
            
        rendered = registry[markup]().render(self.field.to_python(value))
        setattr(obj, self.rendered_name, rendered)
        

class MarkupEditorField(models.TextField):
    """
    A field that stores a Markup Editor.
    """
    def contribute_to_class(self, cls, name):

        choices = get_choices()
        markup_field = models.CharField(choices=choices, null=True, blank=True, max_length=255)
        markup_field.creation_counter = self.creation_counter
        cls.add_to_class('%s_markup' % name, markup_field)

        rendered_field = models.TextField(null=True, blank=True, editable=False)
        rendered_field.creation_counter = self.creation_counter        
        cls.add_to_class('%s_rendered' % name, rendered_field)

        super(MarkupEditorField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MarkupEditorCreator(self))

    def formfield(self, **kwargs):
        defaults = {'widget': MarkupEditorWidget}
        defaults.update(kwargs)
        return super(MarkupEditorField, self).formfield(**defaults)

class MarkupEditorWidget(forms.Textarea):
    class Media:
        css = {
            'all': (
                'css/theme/ui.all.css',
                'css/markupeditor.css',
            )
        }
        js = (
            'js/jquery-1.3.1.js',
            'js/jquery.ui.all.js',
            'js/markupeditor.js',
        )