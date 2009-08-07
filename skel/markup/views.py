from django.shortcuts import render_to_response
from django.template import RequestContext
from skel.markup.engines import registered_engines

def preview(request, engine_name):
    source = request.POST['source']
    engine = registered_engines[engine_name]()
    rendered = engine.render(source)
    return render_to_response('markup/preview.html', {'rendered': rendered},
                              context_instance=RequestContext(request))