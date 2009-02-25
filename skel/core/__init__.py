from django.db.models.signals import class_prepared
from skel.markupeditor.fields import add_extra_fields
from skel.core.models import SkelComment
from skel.core.forms import SkelCommentForm


def extend_flatpages(sender, **kwargs):
    if sender._meta.module_name == 'flatpage':
        from django.db import models
        for f in sender._meta.fields:
            if f.name == 'content':
                add_extra_fields(f, sender, f.name)
                
        
class_prepared.connect(extend_flatpages)


def get_model():
    return SkelComment
    
    
def get_form():
    return SkelCommentForm