from django.http import Http404
from django.views.generic.list_detail import object_detail
from tagging.utils import get_tag

# TODO: Rewrite this view to not make object_detail look up by pk
def tag_detail(request, tag=None, **kwargs):
    """
    A thin wrapper around
    ``django.views.generic.list_detail.object_detail`` which looks up
    a given tag by name.
    """
    if tag is None:
        try:
            tag = kwargs.pop('tag')
        except KeyError:
            raise AttributeError('tag_detail must be called with a tag.')

    tag_instance = get_tag(tag)
    if tag_instance is None:
        raise Http404('No Tag found matching "%s".' % tag)
    return object_detail(request, object_id=tag_instance.pk, **kwargs)