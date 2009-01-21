from django.contrib import admin
from django.conf import settings
from blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'content',
                'tags',
                'author',
                'public',
                'sites',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'summary',
                'content_html',
                'slug',
                'published',
            )
        }),
    )
    list_display = ('published', 'title', 'author', 'public',)
    list_filter = ('author', 'public', 'sites',)
    search_fields = ['title', 'content',]
    
    def queryset(self, request):
        qs = self.model.admin_manager.get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(EntryAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['author'].initial = request.user.pk
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(Entry, EntryAdmin)