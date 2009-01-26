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

BLOG_MORE_RE = re.compile('(?P<summary>.*?)\s*((&lt;)|<)!--\s*more\s*--(>|(&gt;))(?P<the_rest>.*)', re.S)

class PublicEntryManager(models.Manager):
    def get_query_set(self):
        return super(PublicEntryManager, self).get_query_set().filter(
        public__exact=True, sites__id__exact=settings.SITE_ID)

class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text='Use Markdown syntax.')
    summary = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    tags = TagField()
    content_html = models.TextField(blank=True)
    public = models.BooleanField(default=True)
    slug = models.SlugField(unique_for_date='published')
    sites = models.ManyToManyField(Site)
    objects = PublicEntryManager()
    admin_manager = models.Manager()
    
    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-published',)
        get_latest_by = 'published'
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        matches = BLOG_MORE_RE.search(self.content)
        if matches is None:
            summary_words = getattr(settings, 'BLOG_SUMMARY_WORD_COUNT', 300)
            self.summary = truncate_html_words(self.content, summary_words)
        else:
            self.summary = matches.groupdict()['summary'] + '...'
        self.summary = markdown.markdown(self.summary, ['codehilite'])
        self.content_html = matches.groupdict()['summary'] + matches.groupdict()['the_rest']
        self.content_html = markdown.markdown(self.content_html, ['codehilite'])
        super(Entry, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog-detail', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.strftime('%d'),
            'slug': self.slug,
        })
    
    @property
    def comments_enabled(self):
        if not self.public:
            return False
        max_age = getattr(settings, 'BLOG_AUTO_CLOSE_COMMENTS', 60)
        if isinstance(max_age, int) and max_age > 0:
            delta = datetime.datetime.now() - self.published
            return delta.days < max_age
        return True

def format_comment(sender, comment, request, **kwargs):
    comment.comment = markdown.markdown(comment.comment, ['codehilite'])
    comment.save()

def moderate_comment(sender, comment, request, **kwargs):
    if not comment.content_object.comments_enabled:
        comment.is_public = False
        comment.save()

comment_was_posted.connect(format_comment)
comment_was_posted.connect(moderate_comment)