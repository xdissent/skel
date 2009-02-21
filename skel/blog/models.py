import markdown
import re
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import truncate_html_words
from django.contrib.comments.signals import comment_was_posted
from django.contrib.sites.models import Site
from tagging.fields import TagField
from skel.core.models import Image, PublicSitesObjectManager
from skel.markupeditor.fields import MarkupEditorField
from skel import categories

class Entry(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    tags = TagField(blank=True)
    slug = models.SlugField(unique_for_date='published')
    sites = models.ManyToManyField(Site)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    images = models.ManyToManyField(Image, blank=True, null=True)
    summary = MarkupEditorField(blank=True)
    body = MarkupEditorField()
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
        if not self.public:
            return False
        max_age = getattr(settings, 'BLOG_AUTO_CLOSE_COMMENTS', False)
        if max_age and max_age > 0:
            delta = datetime.datetime.now() - self.published
            return delta.days < max_age
        return True


def format_comment(sender, comment, request, **kwargs):
    #comment.comment = markdown.markdown(comment.comment, ['codehilite'])
    comment.save()


def moderate_comment(sender, comment, request, **kwargs):
    if not comment.content_object.comments_enabled:
        comment.is_public = False
        comment.save()


comment_was_posted.connect(format_comment)
comment_was_posted.connect(moderate_comment)

categories.register(Entry)