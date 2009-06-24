from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from skel.accounts.models import UserProfile
from skel.markupeditor.fields import MarkupEditorField, MarkupEditorWidget

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
    model_admin_manager = UserProfile.admin_manager
    formfield_overrides = {
        MarkupEditorField: {'widget': MarkupEditorWidget},
    }

class SkelUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, SkelUserAdmin)