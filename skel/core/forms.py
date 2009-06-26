from django import forms
from django.contrib.comments.forms import CommentForm
from django.contrib.flatpages.admin import FlatpageForm
from skel.core import settings



from skel.markupeditor.markups import get_choices
from skel.markupeditor.fields import MarkupEditorWidget

choices = [('', '---------')] + get_choices()
    

class SkelCommentForm(CommentForm):
    comment = forms.CharField(widget=MarkupEditorWidget)
    comment_markup = forms.TypedChoiceField(choices=choices, required=False)
    
    def get_comment_model(self):
        from skel.core.models import SkelComment
        return SkelComment

    def get_comment_create_data(self):
        data = super(SkelCommentForm, self).get_comment_create_data()
        data['comment_markup'] = self.cleaned_data['comment_markup']
        return data

    
class SkelFlatpageForm(FlatpageForm):
    content = forms.CharField(widget=MarkupEditorWidget)