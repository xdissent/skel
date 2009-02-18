from django.contrib import admin
from django.conf import settings
from skel.blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'public',
                'author',
                'categories',
                'tags',
                'sites',
                'images',
                'summary',
                'summary_markup',
                'body',
                'body_markup',
                
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'published',
            )
        }),
    )
    list_display = ('published', 'title', 'author', 'body_markup', 'public',)
    list_filter = ('author', 'public', 'sites', 'categories', 'tags')
    search_fields = ['title', 'body', 'summary']
    model_admin_manager = Entry.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(EntryAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['author'].initial = request.user.pk
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Entry, EntryAdmin)