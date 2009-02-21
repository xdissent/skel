from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404
from skel.categories.models import Category

def category_object_list(request, slug, *args, **kwargs):
    category = get_object_or_404(Category, slug=slug)
    queryset = kwargs.pop('queryset')
    categories_field = kwargs.pop('categories_field', 'categories')
    filter_kwargs = {}
    filter_kwargs[categories_field] = category
    kwargs['queryset'] = queryset.filter(**filter_kwargs)
    extra_context = kwargs.pop('extra_context', {})
    extra_context['category'] = category
    kwargs['extra_context'] = extra_context
    return object_list(request, *args, **kwargs)