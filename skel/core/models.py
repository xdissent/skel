# TODO: Integrate django.contrib.sites into Image Managers
# done: Combine Image and Category Managers and export to other apps

from django.db import models
from django.conf import settings
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.comments.managers import CommentManager
from django.contrib.auth.models import User
from skel.core.managers import PublicObjectManager
from skel.superimage.fields import SuperImageField
from skel.markupeditor.fields import MarkupEditorField
        

# TODO: Figure out to change filename through M2M field
def upload_to(instance, filename):
    # print instance._meta.__dict__
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
