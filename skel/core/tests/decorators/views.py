from django.shortcuts import render_to_response
from skel.core.decorators import ajaxable

@ajaxable
def ajaxable_view(request, template_name=None):
    return render_to_response(template_name)
    
@ajaxable(template_name='core/tests/decorators/ajaxable_xhr.html')
def ajaxable_view_template_name(request, template_name=None):
    if template_name is None:
        template_name = 'core/tests/decorators/ajaxable.html'
    return render_to_response(template_name)
    
@ajaxable
def ajaxable_view_no_kwarg(request, template_name='core/tests/decorators/ajaxable.html'):
    return render_to_response(template_name)
    
@ajaxable
def ajaxable_view_no_kwarg_no_default(request, **kwargs):
    """
    This view only accepts the ``template_name`` keyword argument implicitly 
    and the ``ajaxable`` decorator will have no effect if it cannot figure 
    out an appropriate template to use.
    """
    template_name = kwargs.get('template_name', 'core/tests/decorators/ajaxable.html')
    return render_to_response(template_name)