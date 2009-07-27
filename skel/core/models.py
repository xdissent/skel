from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from skel.core.managers import NavigationMenuManager

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.managers import CommentManager
from django.contrib.comments.models import BaseCommentAbstractModel
from skel.markupeditor.fields import MarkupEditorField

# TODO: Clean this model up
class SkelComment(BaseCommentAbstractModel):
    """
    A user comment about some object.
    """
    user = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_comments")
    user_name = models.CharField(max_length=50, blank=True)
    user_email = models.EmailField(blank=True)
    user_url = models.URLField(blank=True)

    comment = MarkupEditorField()
    
    submit_date = models.DateTimeField(default=None)
    ip_address  = models.IPAddressField(blank=True, null=True)
    is_public   = models.BooleanField(default=True,
                    help_text='Uncheck this box to make the comment effectively ' \
                                'disappear from the site.')
    is_removed  = models.BooleanField(default=False,
                    help_text='Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.')

    objects = CommentManager()

    class Meta:
        db_table = 'skel_comments'
        ordering = ('submit_date',)
        permissions = [('can_moderate', 'Can moderate comments')]

    def __unicode__(self):
        return '%s: %s...' % (self.name, self.comment[:50])

    def save(self, force_insert=False, force_update=False):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(SkelComment, self).save(force_insert, force_update)

    def _get_userinfo(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, '_userinfo'):
            self._userinfo = {
                'name'  : self.user_name,
                'email' : self.user_email,
                'url'   : self.user_url
            }
            if self.user_id:
                u = self.user
                if u.email:
                    self._userinfo['email'] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    self._userinfo['name'] = self.user.get_full_name()
                elif not self.user_name:
                    self._userinfo['name'] = u.username
        return self._userinfo
    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)

    def _get_name(self):
        return self.userinfo['name']
    def _set_name(self, val):
        if self.user_id:
            raise AttributeError('This comment was posted by an authenticated '\
                                   'user and thus the name is read-only.')
        self.user_name = val
    name = property(_get_name, _set_name, doc='The name of the user who posted this comment')

    def _get_email(self):
        return self.userinfo['email']
    def _set_email(self, val):
        if self.user_id:
            raise AttributeError('This comment was posted by an authenticated '\
                                   'user and thus the email is read-only.')
        self.user_email = val
    email = property(_get_email, _set_email, doc='The email of the user who posted this comment')

    def _get_url(self):
        return self.userinfo['url']
    def _set_url(self, val):
        self.user_url = val
    url = property(_get_url, _set_url, doc='The URL given by the user who posted this comment')

    def get_absolute_url(self, anchor_pattern='#c%(id)s'):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user or self.name,
            'date': self.submit_date,
            'comment': self.comment,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return 'Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s' % d


class SkelCommentFlag(models.Model):
    user      = models.ForeignKey(User, verbose_name='user', related_name='skel_comment_flags')
    comment   = models.ForeignKey(SkelComment, verbose_name='comment', related_name='flags')
    flag      = models.CharField('flag', max_length=30, db_index=True)
    flag_date = models.DateTimeField('date', default=None)

    # Constants for flag types
    SUGGEST_REMOVAL = 'removal suggestion'
    MODERATOR_DELETION = 'moderator deletion'
    MODERATOR_APPROVAL = 'moderator approval'

    class Meta:
        db_table = 'skel_comment_flags'
        unique_together = [('user', 'comment', 'flag')]
        verbose_name = 'comment flag'
        verbose_name_plural = 'comment flags'

    def __unicode__(self):
        return '%s flag of comment ID %s by %s' % \
            (self.flag, self.comment_id, self.user.username)

    def save(self, force_insert=False, force_update=False):
        if self.flag_date is None:
            self.flag_date = datetime.datetime.now()
        super(SkelCommentFlag, self).save(force_insert, force_update)


class NavigationMenu(models.Model):
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    children = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='parents')
    public = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)

    objects = NavigationMenuManager()
    admin_manager = models.Manager()
    
    def __unicode__(self):
        if self.url:
            return '%s (%s)' % (self.label, self.get_absolute_url())
        return self.label
    
    def get_absolute_url(self):
        # TODO: Fix these tests
        if self.url is None:
            return None
        if self.url.startswith('http') or '/' in self.url or self.url.startswith('http'):
            return self.url
        return reverse(self.url)
        
    @property
    def is_root(self):
        return (self.parents)

    
