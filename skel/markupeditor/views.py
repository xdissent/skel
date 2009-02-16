from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from skel.markupeditor.markups import registry


def preview(request, markup):
    #if markup not in registry or 'content' not in request.POST:
    #    raise Http404

    rendered = registry[markup]().render(request.POST['content'])
    
    return render_to_response('markupeditor/preview.html',
                          { 'rendered': rendered },
                          context_instance=RequestContext(request))