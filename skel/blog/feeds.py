from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from skel.blog.models import Entry
from skel.blog import settings


class EntryFeed(Feed):
    title = settings.SKEL_BLOG_FEED_TITLE
    description = settings.SKEL_BLOG_FEED_DESCRIPTION
    description_template = 'blog/feed_description.html'
    
    def link(self):
        return reverse('blog:latest')

    def items(self):
        return Entry.objects.all()[:settings.SKEL_BLOG_FEED_NUM_ITEMS]
    
    def item_author_name(self, item):
        return item.author.get_full_name()
        
    def item_author_email(self, item):
        if settings.SKEL_BLOG_FEED_SHOW_AUTHOR_EMAIL:
            return item.author.email
    
    # TODO: Determine if this should invole profiles
    def item_author_link(self, item):
        return item.author.get_profile().url
    
    def item_pubdate(self, item):
        return item.published
        
    def item_categories(self, item):
        if settings.SKEL_BLOG_CATEGORIES_ENABLED:
            return [category.name for category in item.categories.all()]
        
        
class EntryCategoryFeed(EntryFeed):
    def get_object(self, bits):
        # We want to show a 404 when provided an empty or weird URLs.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        from skel.categories.models import Category
        try:
            return Category.objects.get(slug__exact=bits[0])
        except ObjectDoesNotExist:
            # Instantiate a new Category for use in other methods.
            return Category(slug=bits[0], name=bits[0])
    
    def title(self, obj):
        return settings.SKEL_BLOG_CATEGORY_FEED_TITLE % obj.name
    
    def link(self, obj):
        return reverse('blog:category', args=[obj.slug])

    def items(self, obj):
        if obj.pk is None:
            return []
        return obj.entry_set.all()[:settings.SKEL_BLOG_FEED_NUM_ITEMS]
        
        
class EntryTagFeed(EntryFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        from tagging.models import Tag
        try:
            return Tag.objects.get(name=bits[0])
        except ObjectDoesNotExist:
            return Tag(name=bits[0])
    
    def title(self, obj):
        return settings.SKEL_BLOG_TAG_FEED_TITLE % obj.name
    
    def link(self, obj):
        return reverse('blog:tag', args=[obj])

    def items(self, obj):
        if obj.pk is None:
            return []
        from tagging.models import TaggedItem
        return TaggedItem.objects.get_by_model(Entry, obj)[:settings.SKEL_BLOG_FEED_NUM_ITEMS]