import pdb
from django import forms
from django.forms.util import ErrorList
from django.forms.models import ModelFormMetaclass, ModelForm
from skel.markup.engines import registered_engines
from skel.markup import registered_models, settings


def get_choices(model_name):
    choices = []
    if model_name in settings.SKEL_MARKUP_ENGINES:
        engines = settings.SKEL_MARKUP_ENGINES[model_name]
    else:
        engines = settings.SKEL_MARKUP_ENGINES['']
    for engine_name in engines:
        engine_class = registered_engines[engine_name]
        choices.append([engine_name, engine_class.label])
    return choices


class MarkUpWidget(forms.Select):
    """"""
    class Media:
        js = ('js/markupeditor.js',)


class MarkedUpModelFormMetaclass(ModelFormMetaclass):
    """Metaclass which creates a dynamic form for use with markup engines."""
    def __new__(cls, name, bases, attrs):
        if name is 'MarkedUpModelForm' or 'Meta' not in attrs:
            return super(MarkedUpModelFormMetaclass, cls).__new__(cls, name, 
                                                                  bases, attrs)
        model = attrs['Meta'].model
        model_name = '.'.join([model._meta.app_label, model._meta.module_name])
        
        if model_name not in registered_models:
            return super(MarkedUpModelFormMetaclass, cls).__new__(cls, name, 
                                                                  bases, attrs)
        attrs['markup_fields'] = registered_models[model_name]
        # Add markup engine selection fields.
        for field_name in registered_models[model_name]:
            widget = MarkUpWidget(choices=get_choices(model))
            field = forms.CharField(widget=widget)
            attrs[''.join([field_name, '_markup_engine'])] = field
        # Build form class.
        form = super(MarkedUpModelFormMetaclass, cls).__new__(cls, name, 
                                                              bases, attrs)
        # Add ``markupeditor`` class to marked up fields.
        # FIXME: This doesn't work for admin, which overrides TextFields.
        for field_name in registered_models[model_name]:
            form.base_fields[field_name].widget.attrs['class'] = 'markupeditor'
        return form


class MarkedUpModelForm(ModelForm):
    __metaclass__ = MarkedUpModelFormMetaclass
    
    markup_fields = []
        
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        print 'MarkedUpModelForm __init__()'
        if initial is None:
            initial = {}
        if instance is not None:
            for field in self.markup_fields:
                if field not in initial:
                    engine_field_name = ''.join([field, '_markup_engine'])
                    markedup_attr = ''.join([field, '_markedup'])
                    markedup_item = getattr(instance, markedup_attr)
                    if markedup_item.engine_name:
                        initial[engine_field_name] = markedup_item.engine_name
        super(MarkedUpModelForm, self).__init__(data, files, auto_id, prefix, 
                                                initial, error_class, 
                                                label_suffix, empty_permitted, 
                                                instance)
        
    def save(self, commit=True):
        print 'MarkedUpModelForm save()'
        obj = super(MarkedUpModelForm, self).save(commit=commit)
        
        # Create save_m2m function that renders markup.
        old_m2m = getattr(self, 'save_m2m', None)
        def save_m2m():
            print 'save_m2m'
            if old_m2m is not None:
                old_m2m()
            for field_name in self.markup_fields:
                engine_field_name = ''.join([field_name, '_markup_engine'])
                markedup_attr = ''.join([field_name, '_markedup'])
                markedup_item = getattr(obj, markedup_attr)
                markedup_item.engine_name = self.cleaned_data[engine_field_name]
                markedup_item.render()
                markedup_item.save()
        if commit:
            save_m2m()
        else:
            self.save_m2m = save_m2m
        return obj


def markedup_modelform_factory(model, form=MarkedUpModelForm, 
                               fields=None, exclude=None, 
                               formfield_callback=lambda f: f.formfield()):
    """Create a MarkedUpModelForm subclass for a model.
    
    This factory function returns a dynamically generated subclass
    of MarkedUpModelForm and is especially useful when you don't know
    which model you're dealing with until runtime. Mostly just taken
    from Django.
    
    Example:
    
        from skel.blog.models import Entry
        form = markedup_modelform_factory(Entry)
    
        Equivalent form:
        class MarkedUpEntryForm(MarkedUpModelForm):
            class Meta:
                model = Entry
    
    """
    # Create a Meta class.
    attrs = {'model': model}
    parent = (object,)
    if hasattr(form, 'Meta'):
        parent = (form.Meta, object)
    Meta = type('Meta', parent, attrs)

    # Give this new form class a reasonable name.
    class_name = ''.join(['MarkedUp', model.__name__, 'Form'])

    # Class attributes for the new form class.
    form_class_attrs = {
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }
    return MarkedUpModelFormMetaclass(class_name, (form,), form_class_attrs)