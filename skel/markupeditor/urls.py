from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
#from skel.markupeditor.models import Item

from skel.markupeditor.views import preview

urlpatterns = patterns('',
    url(r'^preview/(?P<markup>[a-z]+)/', preview),
    #url(r'^item/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', { 
    #        'queryset': Item.objects.all(),
    #        'template_name': 'detail.html'
    #}),
)