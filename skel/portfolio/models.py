import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from skel.core.managers import PublicSitesObjectManager
from skel.portfolio import settings
from skel.markupeditor.fields import MarkupEditorField
from tagging.fields import TagField
from massmedia.models import Collection


class Client(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    url = models.URLField(blank=True, verify_exists=True)
    sites = models.ManyToManyField(Site)
    public = models.BooleanField(default=True)
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()
            
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-client-detail', None, {'slug': self.slug})


class Testimonial(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.TextField()
    url = models.URLField(blank=True, verify_exists=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    sites = models.ManyToManyField(Site)
    public = models.BooleanField(default=True)
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()

    def __unicode__(self):
        return '%s - %s' % (self.quotee, self.project.title)


class Project(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    tags = TagField(blank=True)
    media = models.ForeignKey(Collection, blank=True, null=True)
    slug = models.SlugField(unique=True)
    sites = models.ManyToManyField(Site)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    summary = MarkupEditorField(blank=True)
    description = MarkupEditorField()

    testimonials = models.ManyToManyField(Testimonial, blank=True, null=True)
    contributors = models.ManyToManyField(User, blank=True, null=True, related_name='projects_contributes_to')
    maintainers = models.ManyToManyField(User, blank=True, null=True, related_name='projects_maintained')
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, verify_exists=True)
    
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
        
    @property
    def comments_enabled(self):
        if settings.PORTFOLIO_AUTO_CLOSE_COMMENTS_DAYS > 0:
            delta = datetime.datetime.now() - self.published
            return delta.days < settings.PORTFOLIO_AUTO_CLOSE_COMMENTS_DAYS
        return settings.PORTFOLIO_COMMENTS_ENABLED and self.public

# if settings.PORTFOLIO_CATEGORIES_ENABLED:
from skel import categories
categories.register(Project)