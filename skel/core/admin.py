from django.contrib import admin
from django.conf import settings
from skel.core.models import Image


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