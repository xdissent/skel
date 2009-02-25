from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments import get_model
from skel.core.models import Image, SkelComment
from skel.markupeditor.fields import MarkupEditorWidget

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'image',
                'public',
            ),
        }),
    )
    model_admin_manager = Image.admin_manager


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class SkelFlatpageForm(FlatpageForm):
    content = forms.CharField(widget=MarkupEditorWidget)


class SkelFlatPageAdmin(FlatPageAdmin):
    form = SkelFlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'content_markup', 'sites')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )


class SkelCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
            {'fields': ('content_type', 'object_pk', 'site')}
        ),
        ('Content',
            {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment_markup', 'comment')}
        ),
        ('Metadata',
            {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )
    
    
admin.site.register(Image, ImageAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, SkelFlatPageAdmin)
    
if get_model() is SkelComment:
    admin.site.register(SkelComment, SkelCommentsAdmin)