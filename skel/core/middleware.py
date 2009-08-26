from django.core.exceptions import MiddlewareNotUsed

class PoliteMiddleware(object):
    """A base class that makes it easy to conditionally run a middleware."""
    def __init__(self):
        """Initialize the middleware and discard it if appropriate."""
        if not self._should_use():
            raise MiddlewareNotUsed

    def process_request(self, request):
        """Process the request conditionally."""
        if not self._should_process_request(request):
            return None
        return self._process_request(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Process the view conditionally."""
        if not self._should_process_view(request, view_func, view_args, 
                                         view_kwargs):
            return None
        return self.process_view(request, view_func, view_args, view_kwargs)
        
    def process_response(self, request, response):
        """Process the response conditionally."""
        if not self._should_process_response(request, response):
            return response
        return self._process_response(request, response)
        
    def _should_use(self):
        return False
        
    def _should_process_request(self, request):
        return False
    
    def _should_process_view(self, request, view_func, view_args, view_kwargs):
        return False
        
    def _should_process_response(self, request, response):
        return False
                
    def _process_request(self, request):
        raise NotImplementedError
        
    def _process_view(self, request, view_func, view_args, view_kwargs):
        raise NotImplementedError
        
    def _process_response(self, request, response):
        raise NotImplementedError