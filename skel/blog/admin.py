from django.contrib import admin
from skel.markup.admin import MarkedUpAdmin
from skel.blog.models import Entry
from skel.blog import settings


class EntryAdmin(MarkedUpAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('published', 'title', 'author', 'public',)
    search_fields = ['title', 'body', 'summary']
    
    def get_form(self, request, obj=None, **kwargs):
        """Extend the create form to include initial values."""
        form = super(EntryAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            # Set initial author and site.
            form.base_fields['author'].initial = request.user.pk
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form
        

admin.site.register(Entry, EntryAdmin)