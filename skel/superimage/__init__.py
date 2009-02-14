import os
from PIL import Image
from StringIO import StringIO
from django.core.files.base import ContentFile
from django.db import models


def extract_prefix(prefix, data):
    extracted = {}
    for name in data.keys():
        if name.startswith(prefix):
            ending = name.replace(self.prefix, '')
            extracted[ending] = data[ending]
    return extracted
    

class SuperImage(object):
    def __init__(self, file, name, data):
        self.file = file
        self.name = name
        self.data = data
            

class SuperImagePlugin(object):
    def __init__(self, field):
        self.field = field

    def contribute_to_class(self, field, model, name):
        pass
        
    def apply_to_instance(self, instance, superimage):
        pass

    def reset(self, instance, superimage):
        pass
    
    # TODO: implement
    def render(self, name, value, attrs=None)
        pass
    
    # TODO: implement    
    @property
    def media(self):
         return None 

            
class SuperThumbnailPlugin(SuperImagePlugin):
    """Creates, stores, and manages thumbnails for a SuperImageField"""
    def __init__(self, *args, **kwargs):
        super(SuperImageCropPlugin, self).__init__(*args, **kwargs)
        self.prefix = '%s_thumbnail_' % self.field.name
        self.delete = []
        self.create = []
        self.change = []
    
    def extract_data(self, superimage):
        data = extract_prefix(self.prefix, superimage.data)
        for name in data.keys()
            varname, id = name.split('_', 1)
            val = data[name]
            if val is not None and val != '':
                if id.startswith('new'):
                    if id not in self.create:
                        self.create[id] = {}
                    self.create[id][varname] = val
                else:
                    if id not in self.change:
                        self.change[id] = {}
                    self.change[id][varname] = val
        if 'delete' in data:
            self.delete = data['delete']
                
    def apply_to_instance(self, instance, superimage):
        from skel.superimage.models import Thumbnail
        self.extract_data(superimage)
        thumbnails = getattr(instance, '%s_thumbnails' % self.field.name)
        for title, file in self.create:
            thumb = Thumbnail(title=title)
            thumb.thumbnail.save(self.image.file.name, file, save=False)
            thumb.save()
            thumbnails.add(thumb)
        for id, title in self.change:
            thumb = Thumbnail.objects.get(pk=int(id))
            thumb.title = title
            # TODO: recrop
            thumb.save()
        for id in self.delete:
            thumb = Thumbnail.objects.get(pk=int(id))
            thumb.delete()
            
    def reset(self, instance, superimage):
        thumbnails = getattr(instance, '%s_thumbnails' % self.field.name)
        for thumbnail in thumbnail.all():
            thumbnail.delete()
            
    def contribute_to_class(self, field, cls, name):
        thumbnails_field = models.ManyToManyField(Thumbnail, blank=True, editable=False)
        thumbnails_field.creation_counter = field.creation_counter
        if isinstance(field.upload_to, basestring):
            thumbnails_field.upload_to = os.path.join(field.upload_to, 'thumbnails')
        cls.add_to_class('%s_thumbnails' % name, thumbnails_field)
