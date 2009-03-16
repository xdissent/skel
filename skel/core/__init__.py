# Handle application settings
from django.conf import settings as project_settings
from skel.core.conf import autodiscover, configure_app


if getattr(project_settings, 'CORE_AUTO_APP_SETTINGS', True):
    autodiscover()
else:
    from skel.core import settings as core_settings
    configure_app(core_settings)

from skel.core import settings


# Custom comment functions for settings.COMMENTS_APP = 'skel.core'
def get_model():
    from skel.core.models import SkelComment
    return SkelComment
    
def get_form():
    from skel.core.forms import SkelCommentForm
    return SkelCommentForm


# Comment moderation
def moderate_comment(sender, comment, request, **kwargs):
    if getattr(comment.content_object, 'comments_enabled', 
               settings.CORE_COMMENTS_ENABLED_DEFAULT):
        comment.is_public = False
        comment.save()

if 'django.contrib.comments' in settings.INSTALLED_APPS:
    from django.contrib.comments.signals import comment_was_posted
    comment_was_posted.connect(moderate_comment)
 
    
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
