from django.db import models
from skel.core.managers import PublicObjectManager
from skel import markup

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    objects = PublicObjectManager()
    admin_manager = models.Manager()

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('slug',)

    def __unicode__(self):
        return u'%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('category-detail', None, {
            'slug': self.slug,
        })

markup.register(Category)