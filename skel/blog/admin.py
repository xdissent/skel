from django.contrib import admin
from skel.blog import settings
from skel.blog.models import Entry


entry_fields = [
    'title', 
    'public',
    'author',
    'sites',
    'summary',
    'body',
]

entry_list_filter = ('author', 'public', 'sites')


if settings.BLOG_TAGS_ENABLED:
    entry_fields.append('tags')
    entry_list_filter += ('tags',)


if settings.BLOG_CATEGORIES_ENABLED:
    entry_fields.append('categories')
    entry_list_filter += ('categories',)


if settings.BLOG_MARKUP_ENABLED:
    for field in ('summary', 'body'):
        entry_fields.insert(entry_fields.index(field) + 1, field + '_markup')
        

if settings.BLOG_MEDIA_ENABLED:
    entry_fields.append('media')


class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': entry_fields
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'published',
            )
        }),
    )
    list_display = ('published', 'title', 'author', 'public',)
    list_filter = entry_list_filter
    search_fields = ['title', 'body', 'summary']
    model_admin_manager = Entry.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(EntryAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['author'].initial = request.user.pk
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Entry, EntryAdmin)