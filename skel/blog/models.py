from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from massmedia.models import Collection
from skel.core.managers import PublicSitesObjectManager
from skel.blog import settings
import tagging


class Entry(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='published')
    author = models.ForeignKey(User)
    published = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(auto_now=True)
    tags = tagging.fields.TagField()
    media = models.ForeignKey(Collection, blank=True, null=True)
    summary = models.TextField(blank=True)
    body = models.TextField()
    sites = models.ManyToManyField(Site)
    public = models.BooleanField(default=True)
    
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()
    
    class Meta:
        verbose_name_plural = 'entries'
        ordering = ('-published',)
        get_latest_by = 'published'
    
    def __unicode__(self):
        return u'%s' % self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog:entry', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.strftime('%d'),
            'slug': self.slug,
        })
    
    @property
    def comments_enabled(self):
        if settings.SKEL_BLOG_AUTO_CLOSE_COMMENTS_DAYS > 0:
            delta = datetime.now() - self.published
            return delta.days < settings.SKEL_BLOG_AUTO_CLOSE_COMMENTS_DAYS
        return settings.SKEL_BLOG_COMMENTS_ENABLED and self.public


# Register markup fields.
if settings.SKEL_BLOG_MARKUP_ENABLED:
    from skel import markup
    markup.register(Entry)

# Register tags.
# if SKEL_BLOG_TAGGING_ENABLED:
#     import tagging
#     tagging.register(Entry)

# Register categories.
if settings.SKEL_BLOG_CATEGORIES_ENABLED:
    from skel import categories
    categories.register(Entry)