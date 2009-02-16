from django.contrib import admin
from django.db import models
from skel.superimage.models import Thumbnail

class ThumbnailAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Thumbnail, ThumbnailAdmin)