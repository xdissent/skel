from django.contrib import admin
from skel.categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'public',)
    model_admin_manager = Category.admin_manager

admin.site.register(Category, CategoryAdmin)