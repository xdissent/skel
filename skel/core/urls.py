from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.utils.encoding import force_unicode
from tagging.models import Tag
from skel.core.views import tag_detail, doc_index, doc_skel
import datetime


# TODO: This shouldn't be here
from django import forms
from django.contrib.comments.forms import CommentForm, COMMENT_MAX_LENGTH
from skel.markupeditor.fields import MarkupEditorWidget


def fix_comment_form_init(func):
    def wrapped(self, *args, **kwargs):
        func(self, *args, **kwargs)
        # TODO: Make this not hardcoded
        choices = [('', '---------')] + get_choices()
        self.fields['comment'] = forms.CharField(widget=MarkupEditorWidget(), max_length=COMMENT_MAX_LENGTH)
        self.fields['comment_markup'] = forms.TypedChoiceField(choices=choices, required=False)
    return wrapped


def fix_comment_form_get_comment_object(func):
    def wrapped(self, *args, **kwargs):
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")
    
        new = Comment(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            user_name    = self.cleaned_data["name"],
            user_email   = self.cleaned_data["email"],
            user_url     = self.cleaned_data["url"],
            comment_markup = self.cleaned_data['comment_markup'],
            comment      = self.cleaned_data["comment"],
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
        )

        # This is necessary for MarkupEditorField        
        new.comment = self.cleaned_data['comment']

        # Check that this comment isn't duplicate. (Sometimes people post comments
        # twice by mistake.) If it is, fail silently by returning the old comment.
        possible_duplicates = Comment.objects.filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            user_name = new.user_name,
            user_email = new.user_email,
            user_url = new.user_url,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new
    return wrapped


#CommentForm.__init__ = fix_comment_form_init(CommentForm.__init__)
#CommentForm.get_comment_object = fix_comment_form_get_comment_object(CommentForm.get_comment_object)


tag_dict = {
    'queryset': Tag.objects.all(),
}


urlpatterns = patterns('',
    url(
        r'^tag/(?P<tag>[^/]+)/$', 
        tag_detail,
        tag_dict,
        name='tag-detail',
    ),
    
    url(
        r'^admin/doc/$',
        doc_index,
        {},
        name='django-admindocs-docroot',
    ),
    
    url(
        r'^admin/doc/skel/$',
        doc_skel,
        {},
        name='skel-docroot',
    ),
    
#     url(
#         r'^comments/post/$',
#         post_comment,
#         name='comments-post-comment'
#     ),
)