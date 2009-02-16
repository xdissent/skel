from django.conf.urls.defaults import *
from django.conf import settings
from skel.portfolio.models import Project, Section

project_dict = {
    'queryset': Project.objects.all(),
    'slug_field': 'slug',
}

section_dict = {
    'queryset': Section.objects.all(),
    'slug_field': 'slug',
}

tag_dict = {
    'queryset_or_model': project_dict['queryset'],
    'template_name': 'portfolio/project_tag.html',
    'allow_empty': True,
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$',
        'object_list',
        dict(queryset=section_dict['queryset']),
        name='portfolio-home'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        project_dict,
        name='portfolio-project-detail'
    ),
    url(r'^section/(?P<slug>[-\w]+)/$',
        'object_detail',
        section_dict,
        name='portfolio-section-detail'
    ),
)

urlpatterns += patterns('tagging.views',
    url(r'^tag/(?P<tag>[^/]+)/$',
        'tagged_object_list',
        tag_dict,
        name='portfolio-tag-detail'
    ),
)