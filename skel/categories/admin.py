from django.contrib import admin
from skel.categories.models import Category
from skel.markupeditor.fields import MarkupEditorField, MarkupEditorWidget

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'public',)
    model_admin_manager = Category.admin_manager
    formfield_overrides = {
        MarkupEditorField: {'widget': MarkupEditorWidget},
    }

admin.site.register(Category, CategoryAdmin)