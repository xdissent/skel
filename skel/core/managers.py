from django.conf import settings
from django.db import models


class PublicObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicObjectManager, self).get_query_set().filter(
        public__exact=True)
        

class PublicSitesObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicSitesObjectManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)


class NavigationMenuManager(PublicSitesObjectManager):
    def get_root(self):
        return self.get_query_set().filter(parents__isnull=True)