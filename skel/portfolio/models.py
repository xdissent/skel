import os
import markdown
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from tagging.fields import TagField
from skel.markupeditor.fields import MarkupEditorField
from skel.core.models import Image, Category, PublicSitesObjectManager


class Client(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    url = models.URLField(verify_exists=True)
            
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-client-detail', None, {'slug': self.slug})


class Testimonial(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.TextField()
    client = models.ForeignKey(Client, blank=True, null=True)
    project = models.ForeignKey('Project', blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.quotee, self.project.title)


class Project(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, verify_exists=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    sites = models.ManyToManyField(Site)
    tags = TagField()
    categories = models.ManyToManyField(Category, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True, null=True)
    description = MarkupEditorField()
    summary = MarkupEditorField()
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()
    
    class Meta:
        ordering = ('-published',)
        get_latest_by = 'published'
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-project-detail', None, {'slug': self.slug})