import os
import inspect
from skel.core import settings

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps


class Decorator:
    """A Decorator base class that applies magic to make simple decorators 
    behave more intuitively. 
    
    Subclasses must implement the ``wrapper``
    method, which should call the wrapped function, regardless of how
    the decorator was instantiated. Decorators may accept positional and
    keyword arguments and the ``wrapper`` method receives the arguments 
    passed to the function when called.
    
    """
    def __init__(self, func=None, *args, **kwargs):
        self.func = None
        self.args = None
        self.kwargs = kwargs
        
        if callable(func):
            self.func = func
            update_wrapper(self, func)
        elif func is not None:
            self.args = (func,)
            if args:
                self.args += args
    
    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            @wraps(self.func)
            def _wrapper(*args, **kwargs):
                return self.wrapper(*args, **kwargs)
            return _wrapper
        return self.wrapper(*args, **kwargs)
        
    def get_kwarg_default(self, kwarg_name):
        """Extracts the default value for the keyword argument ``kwarg_name``
        as defined by ``self.func``. 
        
        This method should only be called if ``self.func`` has been already 
        been populated, otherwise it will always raise a ``ValueError``. 
        
        Example::
        
            class RedirectDefaultTemplate(Decorator):
                def wrapper(self, request, *args, **kwargs):
                    if 'template' in kwargs:
                        return self.func(request, *args, **kwargs)
                    template = self.get_kwarg_default('template')
                    template = os.path.join('other_path', template)
                    return self.func(request, template=template, *args, **kwargs)
                
            @RedirectDefaultTemplate    
            def view(request, template='default.html'):
                [...]

        """
        args, varargs, varkw, defaults = inspect.getargspec(self.func)
        return defaults[args.index('template_name') - len(args)]
        
    def wrapper(self, *args, **kwargs):
        """A wrapper for the decorated function.
        
        Subclasses must implement this method. It is called in place of the
        wrapped function and should accept all arguments the function might
        require. This method may assume ``self.args`` and ``self.kwargs``
        have been populated with the arguments passed to the decorator 
        instance and ``self.func`` is the wrapped function.
        
        """
        raise NotImplementedError


class ajaxable(Decorator):
    """AJAX decorator for views that accept the ``template_name`` keyword 
    argument.
    
    When the view is called for an AJAX request, the suffix ``_xhr`` is 
    appended to the original template name (preserving the file extension) 
    and the view is called with the updated ``template_name`` argument. The
    decorator accepts its own ``template_name`` argument which overrides the
    automatically generated name. The ``template_name`` keyword argument 
    must have a default value in the view's definition or you *MUST* pass a
    ``template_name`` to either the view (via ``urls.py``) or the decorator.
    Otherwise, the decorator will have no effect.
    
    Examples::
        
        @ajaxable
        def view(request, template_name='default.html'):
            [...]
            
        @ajaxable(template_name='xhr.html')
        def view(request, template_name=None):
            [...]
        
        # The decorator *may* have no effect on this view:
        @ajaxable
        def view(request, **kwargs):
            [...]

    """
    def wrapper(self, request, template_name=None, *args, **kwargs):
        if not request.is_ajax():
            if template_name is not None:
                return self.func(request, template_name=template_name, 
                                 *args, **kwargs)
            return self.func(request, *args, **kwargs)
        try:
            template_name = self.kwargs.pop('template_name')
        except KeyError:
            if template_name is None:
                try:
                    template_name = self.get_kwarg_default('template_name')
                except ValueError:
                    return self.func(request, *args, **kwargs)
            name, ext = os.path.splitext(template_name)
            template_name = name + settings.SKEL_CORE_AJAXABLE_SUFFIX + ext
        return self.func(request, template_name=template_name, *args, **kwargs)