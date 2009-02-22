from django.http import Http404
from django.views.generic.list_detail import object_detail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admindocs import utils
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admindocs.views import missing_docutils_page, get_root_path
from django.contrib.comments.views.utils import next_redirect
from django.contrib.comments.views.comments import CommentPostBadRequest, post_comment, comment_done
from django.contrib import comments
from django.contrib.comments import signals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve
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
    

def doc_index(request):
    if not utils.docutils_is_available:
        return missing_docutils_page(request)
    return render_to_response('core/admin_doc_index.html', {
        'root_path': get_root_path(),
    }, context_instance=RequestContext(request))
doc_index = staff_member_required(doc_index)


def doc_skel(request):
    pass
    
    
def post_comment(request, next=None):
    """
    Post a comment.

    Wraps ``django.contrib.comments.views.post_comment`` to show errors on
    original object page.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    print data
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    print ctype
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if preview:
        template_list = [
            "comments/%s_%s_preview.html" % tuple(str(model._meta).split(".")),
            "comments/%s_preview.html" % model._meta.app_label,
            "comments/preview.html",
        ]
        return render_to_response(
            template_list, {
                "comment" : form.data.get("comment", ""),
                "form" : form,
            },
            RequestContext(request, {})
        )
        
    if form.errors:
        (view_func, view_args, view_kwargs) = resolve(target.get_absolute_url())
        view_kwargs.update({
            'extra_context': {'comment_form': form}
        })
        return view_func(request, *view_args, **view_kwargs)

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    for (receiver, response) in responses:
        if response == False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    return next_redirect(data, next, comment_done, c=comment._get_pk_val())
