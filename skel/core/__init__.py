from django.db.models.signals import class_prepared
from skel.markupeditor.fields import add_extra_fields

def extend_flatpages(sender, **kwargs):
    if sender._meta.module_name == 'flatpage':
        from django.db import models
        print '%s' % sender._meta.fields
        for f in sender._meta.fields:
            if f.name == 'content':
                add_extra_fields(f, sender, f.name)
    
class_prepared.connect(extend_flatpages)