from django.db import models
from skel.core.managers import PublicObjectManager
from skel.markupeditor.fields import MarkupEditorField

class Category(models.Model):
    """
    A Category.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True)
    description = MarkupEditorField(blank=True)
    public = models.BooleanField(default=True)
    objects = PublicObjectManager()
    admin_manager = models.Manager()

    class Meta:
        ordering = ('slug',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return u'%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('category-detail', None, {
            'slug': self.slug,
        })