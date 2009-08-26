from django.core.exceptions import ImproperlyConfigured
from django.conf.urls.defaults import *
from skel.generic.views import *


# class GenericSuiteBase(object):
#     def __init__(self, queryset=None):
#         if queryset is not None:
#             self.queryset = queryset
# 
#         if self.queryset is None:
#             raise ImproperlyConfigured('Instance requires a queryset.')
#     
#     def get_urls()
# 
#     @property
#     def urls(self):
#         if not hasattr(self, '_urls')
#             setattr(self, '_urls', self.get_urls())
#         return self._urls

class GenericSuite(object):
    """A model based suite with views and URLs."""

    def __init__(self, queryset, current_app='blog', date_field='published'):
        opts = queryset.model._meta
        self.urls = patterns('',
        
            url(r'^/?$', 
                ArchiveView(queryset=queryset, current_app=current_app,
                            date_field=date_field),
                name='archive'),
                
            url(r'^(?P<year>\d{4})/$', 
                YearView(queryset=queryset, current_app=current_app,
                         date_field=date_field, make_object_list=True),
                name='year'),
                
            url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                MonthView(queryset=queryset, current_app=current_app,
                          date_field=date_field, allow_empty=True),
                name='month'),

            url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$', 
                DayView(queryset=queryset, current_app=current_app,
                        date_field=date_field, allow_empty=True),
                name='day'),

            url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                DateDetailView(queryset=queryset, current_app=current_app,
                               date_field=date_field),
                name='detail'),
        )