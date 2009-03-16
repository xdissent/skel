from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from skel.portfolio.models import Project
from skel.portfolio import settings


# TODO: Fill feed attributes from settings (paver should use them too)
class ProjectFeed(Feed):
    title = settings.PORTFOLIO_FEED_TITLE
    description = settings.PORTFOLIO_FEED_DESCRIPTION
    description_template = 'portfolio/feed_description.html'
    
    def link(self):
        return reverse('portfolio-project-latest')

    def items(self):
        return Project.objects.all()[:settings.PORTFOLIO_FEED_NUM_ITEMS]
    
    def item_author_name(self, item):
        return item.author.get_full_name()
        
    def item_author_email(self, item):
        if settings.PORTFOLIO_FEED_SHOW_AUTHOR_EMAIL:
            return item.author.email
    
    # TODO: Determine if this should invole profiles
    def item_author_link(self, item):
        return item.author.get_profile().url
    
    def item_pubdate(self, item):
        return item.published
        
    def item_categories(self, item):
        if settings.PORTFOLIO_CATEGORIES_ENABLED:
            return [category.name for category in item.categories.all()]
        
        
class ProjectCategoryFeed(ProjectFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        from skel.categories.models import Category
        return Category.objects.get(slug__exact=bits[0])
    
    def title(self, obj):
        return settings.PORTFOLIO_CATEGORY_FEED_TITLE % {'category': obj}
    
    def link(self, obj):
        return reverse('portfolio-project-category-detail', args=[obj.slug])

    def items(self, obj):
        return obj.entry_set.all()[:settings.PORTFOLIO_FEED_NUM_ITEMS]
        
        
class ProjectTagFeed(ProjectFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        from tagging.models import Tag
        return Tag.objects.get(name=bits[0])
    
    def title(self, obj):
        return settings.PORTFOLIO_TAG_FEED_TITLE % {'tag': obj}
    
    def link(self, obj):
        return reverse('portfolio-project-tag-detail', args=[obj])

    def items(self, obj):
        from tagging.models import TaggedItem
        return TaggedItem.objects.get_by_model(Project, obj)[:settings.PORTFOLIO_FEED_NUM_ITEMS]