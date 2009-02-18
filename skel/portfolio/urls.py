from django.conf.urls.defaults import *
from django.conf import settings
from tagging.views import tagged_object_list
from skel.portfolio.models import Project

project_dict = {
    'queryset': Project.objects.all(),
}

tag_dict = {
    'queryset_or_model': project_dict['queryset'],
    'template_name': 'portfolio/project_tag.html',
    'allow_empty': True,
}

category_dict = {
    'queryset': Project.objects.all(),
    'slug_field': 'slug',
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
        'django.views.generic.simple.direct_to_template',
        {'template_name': 'nothing.html'},
        name='portfolio-project-category-detail'
    ),
)

