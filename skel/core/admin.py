from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments import get_model
from skel.core import settings
from skel.core.models import NavigationMenu, SkelComment, SkelCommentFlag
from skel.core.forms import SkelFlatpageForm
from skel.markupeditor.fields import MarkupEditorField, MarkupEditorWidget


class NavigationMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'title': ('label',)}
    fieldsets = (
        (None, {'fields': ('label', 'title', 'url', 'public', 'children', 'sites')}),
    )
    list_filter = ('public', 'sites')
    model_admin_manager = NavigationMenu.admin_manager
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(NavigationMenuAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['sites'].initial = (settings.SITE_ID,)
        return form

admin.site.register(NavigationMenu, NavigationMenuAdmin)


# Markup flatpages admin if we're supposed to
class SkelFlatPageAdmin(FlatPageAdmin):
    form = SkelFlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'content_markup', 'sites')}),
        ('Advanced options', {
            'classes': ('collapse',), 
            'fields': ('enable_comments', 'registration_required', 'template_name')
        }),
    )
    formfield_overrides = {
        MarkupEditorField: {'widget': MarkupEditorWidget},
    }
    
if settings.CORE_MARKUP_FLATPAGES:
    from django.contrib.flatpages.models import FlatPage
    admin.site.unregister(FlatPage)
    admin.site.register(FlatPage, SkelFlatPageAdmin)
    
    
comment_fields = ['user', 'user_name', 'user_email', 'user_url', 'comment', 'comment_markup']
class SkelCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
            {'fields': ('content_type', 'object_pk', 'site')}
        ),
        ('Content',
            {'fields': comment_fields}
        ),
        ('Metadata',
            {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )

class SkelCommentFlagsAdmin(admin.ModelAdmin):
    pass
    
if get_model() is SkelComment:
    admin.site.register(SkelComment, SkelCommentsAdmin)
    admin.site.register(SkelCommentFlag, SkelCommentFlagsAdmin)