from django.contrib import admin
from django.conf import settings
from skel.core.models import Image, Category


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
    
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'public',
            ),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
            )
        }),
    )
    model_admin_manager = Category.admin_manager


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)