from django.conf.urls.defaults import *
from django.conf import settings
from tagging.views import tagged_object_list
from skel.portfolio.models import Project
from skel.categories.views import category_object_list

project_dict = {
    'queryset': Project.objects.all(),
}

tag_dict = {
    'queryset_or_model': project_dict['queryset'],
    'template_name': 'portfolio/project_tag_detail.html',
    'allow_empty': True,
}

category_dict = {
    'queryset': Project.objects.all(),
    'template_name': 'portfolio/project_category_detail.html',
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$',
        'object_list',
        project_dict,
        name='portfolio-project-list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        dict(project_dict, slug_field='slug'),
        name='portfolio-project-detail'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        project_dict,
        name='portfolio-project-section-detail'
    ),
)

urlpatterns += patterns('',
    url(r'^tag/(?P<tag>[^/]+)/$',
        tagged_object_list,
        tag_dict,
        name='portfolio-project-tag-detail'
    ),
    url(r'^category/(?P<slug>[^/]+)/$',
        category_object_list,
        category_dict,
        name='portfolio-project-category-detail'
    ),
)

