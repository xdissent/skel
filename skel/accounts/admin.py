from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from skel.accounts.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    max_num = 1

class ProfileUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, ProfileUserAdmin)