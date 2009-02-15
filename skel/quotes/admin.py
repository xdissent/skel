from django.contrib import admin
from django.db import models
from models import Quote


class QuoteAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Quote, QuoteAdmin)