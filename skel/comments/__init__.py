from skel.comments import settings

# Custom comment functions for settings.COMMENTS_APP = 'skel.comments'
def get_model():
    from skel.comments.models import SkelComment
    return SkelComment
    
def get_form():
    from skel.core.forms import SkelCommentForm
    return SkelCommentForm


# Comment moderation
def moderate_comment(sender, comment, request, **kwargs):
    if not getattr(comment.content_object, 'comments_enabled', 
               settings.COMMENTS_ENABLED_DEFAULT):
        comment.is_public = False
        comment.save()
        
def akismet_moderate_comment(sender, comment, request, *args, **kwargs):
    from django.contrib.sites.models import Site
    from django.conf import settings
    
    if request.user.is_authenticated():
        return

    try:
        from akismet import Akismet
    except:
        return

    ak = Akismet(
        key = settings.AKISMET_API_KEY,
        blog_url = 'http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )
    
    if not ak.verify_key():
        return
        
    data = {
        'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'referrer': request.META.get('HTTP_REFERER', ''),
        'comment_type': 'comment',
        'comment_author': comment.user_name.encode('utf-8'),
    }

    if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
        comment.flags.create(
            user=comment.content_object.author,
            flag='spam'
        )
        comment.is_public = False
        comment.save()


if 'django.contrib.comments' in settings.INSTALLED_APPS:
    from django.contrib.comments.signals import comment_was_posted
    comment_was_posted.connect(moderate_comment)
    comment_was_posted.connect(akismet_moderate_comment)
