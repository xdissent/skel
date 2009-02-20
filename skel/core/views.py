from django.http import Http404
from django.views.generic.list_detail import object_detail
from tagging.utils import get_tag
from skel.core.models import Category

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
    
    
from tagging.utils import get_tag, get_queryset_and_model


def category_object_list(request, queryset=None, **kwargs):
    """
    A thin wrapper around
    ``django.views.generic.list_detail.object_list`` which creates a
    ``QuerySet`` containing instances of the given queryset or model
    tagged in the given category.

    In addition to the context variables set up by ``object_list``, a
    ``category`` context variable will contain the ``Category`` instance 
    for the category.
    """
    if queryset is None:
        try:
            queryset = kwargs.pop('queryset')
        except KeyError:
            raise AttributeError(_('category_object_list must be called with a queryset.'))

    if slug is None:
        try:
            slug = kwargs.pop('slug')
        except KeyError:
            raise AttributeError(_('category_object_list must be called with a category slug.'))

    category_instance = Category.objects.filter(slug=slug)
    if category_instance is None:
        raise Http404(_('No Category found matching "%s".') % slug)
    queryset = TaggedItem.objects.get_by_model(queryset_or_model, tag_instance)
    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tag'] = tag_instance
    if related_tags:
        kwargs['extra_context']['related_tags'] = \
            Tag.objects.related_for_model(tag_instance, queryset_or_model,
                                          counts=related_tag_counts)
    return object_list(request, queryset, **kwargs)