from django.contrib.syndication.feeds import Feed
from blog.models import Entry
import datetime

class EntryFeed(Feed):
    title = "The Django weblog"
    link = "http://www.djangoproject.com/weblog/"
    description = "Latest news about Django, the Python Web framework."

    def items(self):
        return Entry.objects.filter(published__lte=datetime.datetime.now())[:10]

    def item_pubdate(self, item):
        return item.published