from django.contrib import admin
from skel.quotes.models import Quote
from skel.markup.admin import MarkedUpAdmin

admin.site.register(Quote, MarkedUpAdmin)