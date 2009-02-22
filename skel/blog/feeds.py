from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from skel.blog.models import Entry
from skel.categories.models import Category
from tagging.models import Tag, TaggedItem


# TODO: Fill feed attributes from settings (paver should use them too)
class EntryFeed(Feed):
    title = 'Hartzog Skel Blog'
    description = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    description_template = 'blog/feed_description.html'
    
    def link(self):
        return reverse('blog-entry-latest')

    def items(self):
        return Entry.objects.all()[:10]
    
    def item_author_name(self, item):
        return item.author.get_full_name()
        
    def item_author_email(self, item):
        return item.author.email
        
    def item_author_link(self, item):
        return item.author.get_profile().url
    
    def item_pubdate(self, item):
        return item.published
        
    def item_categories(self, item):
        return [category.name for category in item.categories.all()]
        
        
class EntryCategoryFeed(EntryFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])
    
    def title(self, obj):
        return 'Hartzog Skel Blog - %s Category' % obj.name
    
    def link(self, obj):
        return reverse('blog-entry-category-detail', args=[obj.slug])

    def items(self, obj):
        return obj.entry_set.all()[:10]
        
        
class EntryTagFeed(EntryFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name=bits[0])
    
    def title(self, obj):
        return 'Hartzog Skel Blog - Entries tagged "%s"' % obj
    
    def link(self, obj):
        return reverse('blog-entry-tag-detail', args=[obj])

    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry, obj)