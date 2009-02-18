# TODO: Integrate django.contrib.sites into Image and Category & Managers
# TODO: Combine Image and Category Managers and export to other apps

from django.db import models
from django.conf import settings
from skel.superimage.fields import SuperImageField
from skel.markupeditor.fields import MarkupEditorField


class PublicObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicObjectManager, self).get_query_set().filter(
        public__exact=True)
        

class PublicSitesObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublicSitesObjectManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)
        

# TODO: Figure out to change filename through M2M field
def upload_to(instance, filename):
    print instance._meta.__dict__
    return 'img/uploads/%s' % filename


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = SuperImageField(upload_to=upload_to, height_field='height', width_field='width')
    width = models.IntegerField(blank=True, null=True, editable=False)
    height = models.IntegerField(blank=True, null=True, editable=False)
    public = models.BooleanField(default=True)
    objects = PublicObjectManager()
    admin_manager = models.Manager()
    
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.image.name)
        
    @models.permalink
    def get_absolute_url(self):
        return self.image.url


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = MarkupEditorField(blank=True)
    public = models.BooleanField(default=True)
    objects = PublicObjectManager()
    admin_manager = models.Manager()
    
    class Meta:
        db_table = 'core_categories'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return u'%s' % (self.title)
        
    @models.permalink
    def get_absolute_url(self):
        return ('category-detail', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.strftime('%d'),
            'slug': self.slug,
        })