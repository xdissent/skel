from django.core import paginator
from django.contrib.sitemaps import Sitemap


class Sitemap(Sitemap):
    def _get_paginator(self):
        return paginator.Paginator(self.items(), self.limit)


class GenericSitemap(Sitemap):
    priority = None
    changefreq = None

    def __init__(self, info_dict, priority=None, changefreq=None):
        self.queryset = info_dict['queryset']
        self.date_field = info_dict.get('date_field', None)
        self.priority = priority
        self.changefreq = changefreq

    def items(self):
        # Make sure to return a clone; we don't want premature evaluation.
        return self.queryset.filter()

    def lastmod(self, item):
        if self.date_field is not None:
            return getattr(item, self.date_field)
        return None