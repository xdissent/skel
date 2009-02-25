from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from skel.core.managers import PublicSitesObjectManager

class Quote(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.TextField()
    sites = models.ManyToManyField(Site)
    public = models.BooleanField(default=True)
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()
