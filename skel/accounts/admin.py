from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from skel.accounts.models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

class SkelUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, SkelUserAdmin)