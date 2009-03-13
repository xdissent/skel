from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments import get_model
from skel.core import settings
from skel.core.models import NavigationMenu, SkelComment
from skel.core.forms import SkelFlatpageForm


admin.site.register(NavigationMenu)


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
    
if settings.CORE_MARKUP_FLATPAGES:
    from django.contrib.flatpages.models import FlatPage
    admin.site.unregister(FlatPage)
    admin.site.register(FlatPage, SkelFlatPageAdmin)
    
    
# Handle comments admin if required
comment_fields = ['user', 'user_name', 'user_email', 'user_url', 'comment']

if settings.CORE_MARKUP_COMMENTS:
    comment_fields.append('comment_markup')

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
    
if get_model() is SkelComment:
    admin.site.register(SkelComment, SkelCommentsAdmin)