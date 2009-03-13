from django import forms
from django.contrib.comments.forms import CommentForm
from django.contrib.flatpages.admin import FlatpageForm
from skel.core import settings


if settings.CORE_MARKUP_COMMENTS:
    from skel.markupeditor.markups import get_choices
    from skel.markupeditor.fields import MarkupEditorWidget
    
    choices = [('', '---------')] + get_choices()
    comment_field = forms.CharField(widget=MarkupEditorWidget)
    markup_field = forms.TypedChoiceField(choices=choices, required=False)
else:
    comment_field = forms.CharField()
    markup_field = None
    

class SkelCommentForm(CommentForm):
    comment = comment_field
    comment_markup = markup_field
    
    def get_comment_model(self):
        from skel.core.models import SkelComment
        return SkelComment

    def get_comment_create_data(self):
        data = super(SkelCommentForm, self).get_comment_create_data()
        if settings.CORE_MARKUP_COMMENTS:
            data['comment_markup'] = self.cleaned_data['comment_markup']
        return data


if settings.CORE_MARKUP_FLATPAGES:        
    from skel.markupeditor.fields import MarkupEditorWidget
    flatpage_content_field = forms.CharField(widget=MarkupEditorWidget)
else:
    flatpage_content_field = forms.CharField()
    
class SkelFlatpageForm(FlatpageForm):
    content = flatpage_content_field