from django.contrib import admin
from skel.categories.models import Category
from skel.markup.admin import MarkedUpAdmin

class CategoryAdmin(MarkedUpAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'public',)

admin.site.register(Category, CategoryAdmin)