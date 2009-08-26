from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.views.generic.list_detail import object_detail
from django.views.static import serve
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admindocs import utils
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.admindocs.views import missing_docutils_page, get_root_path
from tagging.utils import get_tag


def server_error(request, template_name='500.html'):
    """500 error handler.
    
    Templates: `500.html`
    Context: None
    
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return HttpResponseServerError(t.render(RequestContext(request, {})))


def static_server(*args, **kwargs):
    try:
        return serve(*args, **kwargs)
    except Http404:
        return HttpResponseNotFound('Not Found')


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
    
    
# TODO: Implement this
def doc_index(request):
    if not utils.docutils_is_available:
        return missing_docutils_page(request)
    return render_to_response('core/admin_doc_index.html', {
        'root_path': get_root_path(),
    }, context_instance=RequestContext(request))
doc_index = staff_member_required(doc_index)


# TODO: Implement this
def doc_skel(request):
    pass