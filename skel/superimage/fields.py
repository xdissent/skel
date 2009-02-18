from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.db.models.fields.files import ImageFieldFile, FileDescriptor
from django.core.files.uploadedfile import UploadedFile, SimpleUploadedFile
from skel.superimage import SuperImage, SuperImageThumbnailPlugin


# TODO: get media and html from all plugins somehow. attrs?
class SuperImageWidget(forms.FileInput):
    class Media:
        js = (
            'js/jquery/jquery.js',
            'js/jquery/jquery.ui.all.js',
            'js/jquery.jcrop.min.js',
            'js/hartzog/hz.superimage.js',
            'js/admin/superimagewidget.js',
        )
        css = {
            'screen': (
                'css/theme/ui.all.css',
            )
        }
    
    def render(self, name, value, attrs=None):
        rendered = render_to_string('superimage/superimagewidget.html', {
                'image': value, 
                'name': name, 
                'attrs': attrs
        })
        return mark_safe(rendered)
        
    def value_from_datadict(self, data, files, name):
        if files.get(name, None):
            return super(SuperImageWidget, self).value_from_datadict(data, files, name)
        file = super(SuperImageWidget, self).value_from_datadict(data, files, name)
        
        # TODO: determine when to send null for inline editing
        return SuperImage(file, name, data)

        
class SuperImageFormField(forms.ImageField):
    widget = SuperImageWidget
    
    def clean(self, data, initial=None):
        if isinstance(data, SuperImage):
            data.file = super(SuperImageFormField, self).clean(data.file, initial)
        else:
            data = super(SuperImageFormField, self).clean(data, initial)
        return data


# TODO: give all plugins a chance for this
class SuperImageFieldFile(ImageFieldFile):
    """attr_class for SuperImageField that provides instance.superimagefield.thumbnails"""
    def _get_thumbnails(self):
        return getattr(self.instance, '%s_thumbnails' % self.field.name)
    thumbnails = property(_get_thumbnails) 
            
            
class SuperImageFileDescriptor(FileDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, SuperImage):
            for plugin in self.field.plugins:
                plugin.apply_to_instance(instance, value)
            value = value.file
        elif isinstance(value, UploadedFile):
            for plugin in self.field.plugins:
                plugin.reset(instance, value)
            
        instance.__dict__[self.field.name] = value    


class SuperImageField(models.ImageField):
    """Model field that behaves sorta like an image"""
    attr_class = SuperImageFieldFile
    
    def __init__(self, *args, **kwargs):
        super(SuperImageField, self).__init__(*args, **kwargs)
        plugin_classes = kwargs.pop('plugins', (SuperImageThumbnailPlugin,))
        self.plugins = [plugin(self) for plugin in plugin_classes]
    
    def contribute_to_class(self, cls, name):
        super(SuperImageField, self).contribute_to_class(cls, name)
        for plugin in self.plugins:
            plugin.contribute_to_class(cls, name)
        setattr(cls, self.name, SuperImageFileDescriptor(self))
        
    def formfield(self, **kwargs):
        defaults = {'form_class': SuperImageFormField}
        defaults.update(kwargs)
        return super(SuperImageField, self).formfield(**defaults)