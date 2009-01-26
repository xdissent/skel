import os
import markdown
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from tagging.fields import TagField
from PIL import Image as PILImage
from StringIO import StringIO


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
    client = models.ForeignKey(Client, blank=True)
    project = models.ForeignKey('Project', blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.quotee, self.project.title)
        

class PublicProjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicProjectManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)


class Project(models.Model):
    title = models.CharField(max_length=255)
    client = models.ForeignKey(Client, blank=True)
    role = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, verify_exists=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    tags = TagField()
    content = models.TextField(help_text='Use Markdown syntax.')
    content_html = models.TextField(blank=True)
    images = models.ManyToManyField('Image', through='ImageOwnership')
    public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    sites = models.ManyToManyField(Site)
    objects = PublicProjectManager()
    admin_manager = models.Manager()
    
    class Meta:
        ordering = ('-published',)
        get_latest_by = 'published'
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.content_html = markdown.markdown(self.content, ['codehilite'])
        super(Project, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-project-detail', None, {'slug': self.slug})
        

class Section(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    projects = models.ManyToManyField(Project, through='SectionMembership')
    order = models.PositiveIntegerField(blank=True)
    
    class Meta:
        ordering = ('order',)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-section-detail', None, {'slug': self.slug})
    
    
class SectionMembership(models.Model):
    section = models.ForeignKey(Section)
    project = models.ForeignKey(Project)
    order = models.PositiveSmallIntegerField(blank=True)


class Image(models.Model):
    title = models.CharField(max_length=255)
    original = models.ImageField(upload_to='portfolio/projects', height_field='original_height', width_field='original_width')
    original_width = models.IntegerField(editable=False)
    original_height = models.IntegerField(editable=False)
    thumb = models.ImageField(editable=False, upload_to='portfolio/projects/thumbs', height_field='thumb_height', width_field='thumb_width')
    thumb_width = models.IntegerField(editable=False)
    thumb_height = models.IntegerField(editable=False)
    
    def save(self, *args, **kwargs):
        thumb_size = getattr(settings, 'PORTFOLIO_PROJECT_THUMB_SIZE', (100, 100))
        image = PILImage.open(self.original.path)
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        image.thumbnail(thumb_size, PILImage.ANTIALIAS)
        fp = StringIO()
        image.save(fp, image.format)
        cf = ContentFile(fp.getvalue())
        self.thumb.save(name=self.original.name, content=cf, save=False)
        super(Image, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '%s - %s' % (self.title, self.original.name)
    
    
class ImageOwnership(models.Model):
    image = models.ForeignKey(Image)
    project = models.ForeignKey(Project)
    order = models.PositiveSmallIntegerField(blank=True)