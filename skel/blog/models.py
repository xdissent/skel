import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from skel.core.managers import PublicSitesObjectManager
from skel.blog import settings


if settings.BLOG_MARKUP_ENABLED:
    from skel.markupeditor.fields import MarkupEditorField
    text_field_class = MarkupEditorField
else:
    text_field_class = models.TextField


if settings.BLOG_TAGS_ENABLED:
    from tagging.fields import TagField
    tags_field = TagField(blank=True)
else:
    tags_field = None


if settings.BLOG_MEDIA_ENABLED:
    from massmedia.models import Collection
    media_field = models.ForeignKey(Collection, blank=True, null=True)
else:
    media_field = None


class Entry(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    tags = tags_field
    media = media_field
    slug = models.SlugField(unique_for_date='published')
    sites = models.ManyToManyField(Site)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    summary = text_field_class(blank=True)
    body = text_field_class()
    objects = PublicSitesObjectManager()
    admin_manager = models.Manager()
    
    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-published',)
        get_latest_by = 'published'
    
    def __unicode__(self):
        return u'%s' % self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog-entry-detail', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.strftime('%d'),
            'slug': self.slug,
        })
    
    @property
    def comments_enabled(self):
        if settings.BLOG_AUTO_CLOSE_COMMENTS_DAYS > 0:
            delta = datetime.datetime.now() - self.published
            return delta.days < settings.BLOG_AUTO_CLOSE_COMMENTS_DAYS
        return settings.BLOG_COMMENTS_ENABLED and self.public

if settings.BLOG_CATEGORIES_ENABLED:
    from skel import categories
    categories.register(Entry)