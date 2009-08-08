from django.db import models
from skel.core import settings


class PublicObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicObjectManager, self).get_query_set().filter(
                                            public__exact=True)
        

class PublicSitesObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicSitesObjectManager, self).get_query_set().filter(
                                            public__exact=True,
                                            sites__id__exact=settings.SITE_ID)