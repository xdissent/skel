from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse, HttpResponseServerError
from django.template import Context, Template
from skel.core.utils import render_into_response
from skel.core import settings


class PoliteMiddleware(object):
    def __init__(self):
        if not self._should_use():
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if not self._should_process_response(request, response):
            return response
        return self._process_response(request, response)
        
    def _should_use(self):
        return True
    
    def _should_process_response(self, request, response):
        return True
                
    def _process_response(self, request, response):
        raise NotImplementedError
        

class HTMLValidationMiddleware(PoliteMiddleware):
    def _should_use(self):
        return settings.CORE_VALIDATE_RESPONSE
        
    def _should_process_response(self, request, response):
        return (type(response) == HttpResponse and
                'html' in response['Content-Type'] and
                'disable-validation' not in request.GET and
                request.META['REMOTE_ADDR'] in settings.INTERNAL_IPS)
        
    def _process_response(self, request, response):
        import tidy
        
        parsed = tidy.parseString(response.content, 
                                  settings.CORE_VALIDATE_RESPONSE_OPTIONS)
        if not parsed.errors:
            return response

        lines = []
        error_dict = dict(map(lambda e: (e.line, e.message), parsed.errors))
        for i, line in enumerate(response.content.split('\n')):
            lines.append((line, error_dict.get(i + 1, False)))

        response.content = str(parsed)
        render_into_response(response, 'core/validator_head.html', 
                             target='head', position='last')
        return render_into_response(response, 'core/validator.html', 
                                    {'parsed': parsed, 'lines': lines})