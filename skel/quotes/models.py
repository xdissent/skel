from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

class PublicQuoteManager(models.Manager):
    def get_query_set(self):
        return super(PublicQuoteManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)

class Quote(models.Model):
    quotee = models.CharField(max_length=255)
    quote = models.TextField()
    sites = models.ManyToManyField(Site)
    public = models.BooleanField(default=True)
    objects = PublicQuoteManager()
    admin_manager = models.Manager()
