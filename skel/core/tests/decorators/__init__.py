from django.test import TestCase, Client
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from skel.core.decorators import Decorator, ajaxable

    
class test_dec(Decorator):
    def wrapper(self, *args, **kwargs):
        if self.args:
            args += self.args
        if self.kwargs:
            kwargs.update(self.kwargs)
        return self.func(*args, **kwargs)
    
    
def test_func(*args, **kwargs):
    """
    A test function
    """
    return (args, kwargs)


class DecoratorTestCase(TestCase):

    def setUp(self):        
        func_foo = 'asdf'
        func_bar = '123'
        
        self.func_args = (func_foo,)
        self.func_kwargs = {'bar': func_bar}
        
        dec_foo = 'ASDF'
        dec_bar = '456'

        self.dec_args = (dec_foo,)
        self.dec_kwargs = {'dec_bar': dec_bar}
        
        self.result_args = self.func_args + self.dec_args
        self.result_kwargs = self.func_kwargs.copy()
        self.result_kwargs.update(self.dec_kwargs)
        
    def testNoDecorator(self):
        result_args, result_kwargs = test_func(*self.func_args, **self.func_kwargs)
        
        self.assertEqual(result_args, self.func_args, 'Arguments were modified')
        self.assertEqual(result_kwargs, self.func_kwargs, 'Keyword arguments were modified')
        
    def testNoCall(self):
        # @test_dec
        
        func = test_dec(test_func)
        result_args, result_kwargs = func(*self.func_args, **self.func_kwargs)
        
        self.assertEqual(result_args, self.func_args, 'Arguments were modified')
        self.assertEqual(result_kwargs, self.func_kwargs, 'Keyword arguments were modified')
        self.check_attribs(func)
    
    def testEmptyCall(self):
        # @test_dec()
        
        func = test_dec()(test_func)
        result_args, result_kwargs = func(*self.func_args, **self.func_kwargs)

        self.assertEqual(result_args, self.func_args, 'Arguments were modified')
        self.assertEqual(result_kwargs, self.func_kwargs, 'Keyword arguments were modified')
        self.check_attribs(func)

    def testDecoratorArgs(self):
        # @test_dec(dec_foo)
        
        func = test_dec(*self.dec_args)(test_func)
        result_args, result_kwargs = func(*self.func_args, **self.func_kwargs)

        self.assertEqual(result_args, self.result_args, 'Arguments were not modified')
        self.assertEqual(result_kwargs, self.func_kwargs, 'Keyword arguments were modified')
        self.check_attribs(func)
        
    def testDecoratorKwargs(self):
        # @test_dec(dec_bar='456')
        
        func = test_dec(**self.dec_kwargs)(test_func)
        result_args, result_kwargs = func(*self.func_args, **self.func_kwargs)

        self.assertEqual(result_args, self.func_args, 'Arguments were modified')
        self.assertEqual(result_kwargs, self.result_kwargs, 'Keyword arguments were not modified')
        self.check_attribs(func)
        
    def testDecoratorArgsKwargs(self):
        # @test_dec(dec_foo, dec_bar='456')
        
        func = test_dec(*self.dec_args, **self.dec_kwargs)(test_func)
        result_args, result_kwargs = func(*self.func_args, **self.func_kwargs)

        self.assertEqual(result_args, self.result_args, 'Arguments were not modified')
        self.assertEqual(result_kwargs, self.result_kwargs, 'Keyword arguments were not modified')
        self.check_attribs(func)
        
    def check_attribs(self, func):
        self.assertEqual(func.__module__, test_func.__module__)
        self.assertEqual(func.__name__, test_func.__name__)
        self.assertEqual(func.__doc__, test_func.__doc__)


class AjaxableTestCase(TestCase):
    urls = 'skel.core.tests.decorators.urls'
    
    def setUp(self):
        self.client = Client()
        
    def testAjaxable(self):
        self.check_url(reverse('ajaxable'))
        
    def testAjaxableTemplateName(self):
        self.check_url(reverse('ajaxable-template-name'))
         
    def testAjaxableNoKwargs(self):
        self.check_url(reverse('ajaxable-no-kwarg'))
        
    def testAjaxableNoKwargsNoDefault(self):
        url = reverse('ajaxable-no-kwarg-no-default')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/tests/decorators/ajaxable.html')
        
        response = self.client.get(url, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTemplateNotUsed(response, 'core/tests/decorators/ajaxable_xhr.html')
        self.assertTemplateUsed(response, 'core/tests/decorators/ajaxable.html')
        
    def check_url(self, url):
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/tests/decorators/ajaxable.html')
        
        response = self.client.get(url, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertTemplateUsed(response, 'core/tests/decorators/ajaxable_xhr.html')