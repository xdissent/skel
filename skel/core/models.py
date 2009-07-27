from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from skel.core.managers import NavigationMenuManager
from skel.markupeditor.fields import MarkupEditorField # Needed for south

class SkelComment(models.Model):
    pass

class NavigationMenu(models.Model):
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    children = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='parents')
    public = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)

    objects = NavigationMenuManager()
    admin_manager = models.Manager()
    
    def __unicode__(self):
        if self.url:
            return '%s (%s)' % (self.label, self.get_absolute_url())
        return self.label
    
    def get_absolute_url(self):
        # TODO: Fix these tests
        if self.url is None:
            return None
        if self.url.startswith('http') or '/' in self.url or self.url.startswith('http'):
            return self.url
        return reverse(self.url)
        
    @property
    def is_root(self):
        return (self.parents)

    
