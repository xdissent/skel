from django.conf.urls.defaults import *
from skel.portfolio.models import Project
from skel.portfolio import settings, feeds


project_dict = {
    'queryset': Project.objects.all(),
}

tag_dict = {
    'queryset_or_model': project_dict['queryset'],
    'template_name': 'portfolio/project_tag_detail.html',
    'allow_empty': True,
}

category_dict = {
    'queryset': project_dict['queryset'],
    'template_name': 'portfolio/project_category_detail.html',
    'allow_empty': True,
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


project_feeds = {
    'projects': feeds.ProjectFeed,
}
project_other_feeds = {}


if settings.PORTFOLIO_TAGS_ENABLED:
    urlpatterns += patterns('tagging.views',
        url(r'^tag/(?P<tag>[^/]+)/$',
            'tagged_object_list',
            tag_dict,
            name='portfolio-project-tag-detail'
        ),
    )
    project_other_feeds['tag'] = feeds.ProjectTagFeed


if settings.PORTFOLIO_CATEGORIES_ENABLED:    
    urlpatterns += patterns('skel.categories.views',
        url(r'^category/(?P<slug>[^/]+)/$',
            'category_object_list',
            category_dict,
            name='portfolio-project-category-detail'
        ),
    )
    project_other_feeds['category'] = feeds.ProjectCategoryFeed
    

core_urlpatterns = patterns('',
    url(r'^projects/', include(urlpatterns)),
)


if settings.PORTFOLIO_FEEDS_ENABLED:
    core_urlpatterns += patterns('',
        url(r'^feeds/projects/(?P<url>.*)/$',
            'django.contrib.syndication.views.feed', 
            {'feed_dict': project_other_feeds}
        ),
        url(r'^feeds/(?P<url>.*)/$',
            'django.contrib.syndication.views.feed',
            {'feed_dict': project_feeds},
            name='feed-root'),
    )