from django.conf.urls.defaults import *

urlpatterns = patterns('skel.core.tests.decorators.views',

    url(r'^xhr/$', 
        'ajaxable_view', 
        {'template_name': 'core/tests/decorators/ajaxable.html'}, 
        name='ajaxable'),
        
    url(r'^xhr-template-name/$', 
        'ajaxable_view_template_name', 
        name='ajaxable-template-name'),
        
    url(r'^xhr-no-kwarg/$', 
        'ajaxable_view_no_kwarg', 
        name='ajaxable-no-kwarg'),
        
    url(r'^xhr-no-kwarg-no-default/$', 
        'ajaxable_view_no_kwarg_no_default', 
        name='ajaxable-no-kwarg-no-default'),
)