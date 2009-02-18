from django.contrib import admin
from django.db import models
from models import Quote


class QuoteAdmin(admin.ModelAdmin):
    model_admin_manager = Quote.admin_manager
    
    
admin.site.register(Quote, QuoteAdmin)