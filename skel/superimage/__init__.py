import os
from PIL import Image
from StringIO import StringIO
from django.core.files.base import ContentFile
from skel.superimage.models import Thumbnail


def extract_prefix(prefix, data):
    extracted = {}
    for name in data.keys():
        if name.startswith(prefix):
            ending = name.replace(prefix, '')
            extracted[ending] = data.getlist(name)
            if len(extracted[ending]) <= 1:
                extracted[ending] = data.get(name)
    return extracted
    

class SuperImage(object):
    def __init__(self, file, name, data):
        self.file = file
        self.name = name
        self.data = data
            

class SuperImagePlugin(object):
    def __init__(self, field):
        self.field = field

    def contribute_to_class(self, model, name):
        pass
        
    def apply_to_instance(self, instance, superimage):
        pass

    def reset(self, instance, superimage):
        pass
    
    # TODO: implement
    def render(self, name, value, attrs=None):
        pass
    
    # TODO: implement    
    @property
    def media(self):
         return None 

            
class SuperImageThumbnailPlugin(SuperImagePlugin):
    """Creates, stores, and manages thumbnails for a SuperImageField"""
    def __init__(self, *args, **kwargs):
        super(SuperImageThumbnailPlugin, self).__init__(*args, **kwargs)

    
    def extract_data(self, superimage):
        prefix = '%s_thumbnail_' % self.field.name
        data = extract_prefix(prefix, superimage.data)
        self.create = {}
        self.change = {}
        self.delete = data.pop('delete', [])
        
        for name in data.keys():
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

    
    def crop(self, superimage, box, size):
        superfile = superimage.file
        superfile.seek(0)
        img = Image.open(superimage.file)
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')                            
        fp = StringIO()
        thumb = img.crop(box).resize(size, Image.ANTIALIAS)
        thumb.save(fp, img.format, quality=128)
        return ContentFile(fp.getvalue())
                
    def apply_to_instance(self, instance, superimage):
        self.extract_data(superimage)
        thumbnails = getattr(instance, '%s_thumbnails' % self.field.name)
        for id, obj in self.create.iteritems():
            thumb = thumbnails.create(title=obj['title'])
            thumb.thumbnail.field.upload_to = os.path.join(self.field.upload_to, thumb.thumbnail.field.upload_to)
            box = (
                int(obj['x1']),
                int(obj['y1']),
                int(obj['x2']),
                int(obj['y2']),
            )
            size = (
                int(obj['w']),
                int(obj['h']),
            )
            file = self.crop(superimage, box, size)
            thumb.thumbnail.save(superimage.file.name, file, save=False)
            thumb.x1, thumb.y1, thumb.x2, thumb.y2 = box
            thumb.save()
        for id, obj in self.change.iteritems():
            thumb = thumbnails.get(pk=int(id))
            thumb.title = obj['title']
            try:
                box = (
                    int(obj['x1']),
                    int(obj['y1']),
                    int(obj['x2']),
                    int(obj['y2']),
                )
                size = (
                    int(obj['w']),
                    int(obj['h']),
                )
            except KeyError:
                pass
            else:
                file = self.crop(superimage, box, size)
                thumb.thumbnail.save(superimage.file.name, file, save=False)
            thumb.save()
        for id in self.delete:
            thumb = thumbnails.get(pk=int(id))
            thumb.delete()
        
            
    def reset(self, instance, superimage):
        if instance.pk:
            thumbnails = getattr(instance, '%s_thumbnails' % self.field.name)
            for thumbnail in thumbnails.all():
                thumbnail.delete()
            
    def contribute_to_class(self, model, name):
        from django.db import models
        thumbnails_field = models.ManyToManyField(Thumbnail, blank=True, 
                                                  editable=False)
        thumbnails_field.creation_counter = self.field.creation_counter
        model.add_to_class('%s_thumbnails' % name, thumbnails_field)
