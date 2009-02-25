from django import forms
from django.contrib.comments.forms import CommentForm
from skel.markupeditor.fields import MarkupEditorWidget
from skel.markupeditor.markups import get_choices
from skel.core.models import SkelComment

MARKUP_CHOICES = [('', '---------')] + get_choices()

class SkelCommentForm(CommentForm):
    comment = forms.CharField(widget=MarkupEditorWidget)
    comment_markup = forms.TypedChoiceField(choices=MARKUP_CHOICES, required=False)
    
    def get_comment_model(self):
        return SkelComment

    def get_comment_create_data(self):
        data = super(SkelCommentForm, self).get_comment_create_data()
        data['comment_markup'] = self.cleaned_data['comment_markup']
        return data