from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from skel.markupeditor.fields import MarkupEditorField

class PublicUserProfileManager(models.Manager):
    def get_query_set(self):
        return super(PublicUserProfileManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField(blank=True, verify_exists=True)
    bio = MarkupEditorField(blank=True)
    public = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site)
    objects = PublicUserProfileManager()
    admin_manager = models.Manager()
        
    class Meta:
        pass
            
    def __unicode__(self):
        return u'User profile for %s' % self.user.username
    
    @models.permalink
    def get_absolute_url(self):
        return ('user-detail', None, {
            'user': self.user.username,
        })