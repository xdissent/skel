from django.contrib import admin
from django.conf import settings
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from skel.core.models import Image
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


admin.site.register(Image, ImageAdmin)



class SkelFlatpageForm(FlatpageForm):
    content = forms.CharField(widget=MarkupEditorWidget)

        

class SkelFlatPageAdmin(FlatPageAdmin):
    form = SkelFlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'content_markup', 'sites')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, SkelFlatPageAdmin)