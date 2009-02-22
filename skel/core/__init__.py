from django import forms
from django.db.models.signals import class_prepared
from skel.markupeditor.fields import add_extra_fields, MarkupEditorWidget
from skel.markupeditor.markups import get_choices

def extend_flatpages(sender, **kwargs):
    if sender._meta.module_name == 'flatpage':
        from django.db import models
        for f in sender._meta.fields:
            if f.name == 'content':
                add_extra_fields(f, sender, f.name)
                

def extend_comments(sender, **kwargs):
    if sender._meta.app_label == 'comments' and sender._meta.module_name == 'comment':
        from django.db import models
        for f in sender._meta.fields:
            if f.name == 'comment':
                add_extra_fields(f, sender, f.name)


class_prepared.connect(extend_flatpages)
class_prepared.connect(extend_comments)