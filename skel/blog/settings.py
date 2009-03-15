from django.conf import settings


BLOG_MARKUP_ENABLED = ('skel.markupeditor' in settings.INSTALLED_APPS)

BLOG_MEDIA_ENABLED = ('massmedia' in settings.INSTALLED_APPS)

BLOG_TAGS_ENABLED = ('tagging' in settings.INSTALLED_APPS)

BLOG_CATEGORIES_ENABLED = ('skel.categories' in settings.INSTALLED_APPS)

BLOG_COMMENTS_ENABLED = ('django.contrib.comments' in settings.INSTALLED_APPS)

BLOG_AUTO_CLOSE_COMMENTS_DAYS = 60

BLOG_FEEDS_ENABLED = True

BLOG_FEED_TITLE = 'Skel Blog Feed'

BLOG_FEED_DESCRIPTION = 'Skel Blog Feed'

BLOG_FEED_NUM_ITEMS = 10

BLOG_FEED_SHOW_AUTHOR_EMAIL = False

BLOG_CATEGORY_FEED_TITLE = '%s - %%(category.title)s Category' % BLOG_FEED_TITLE

BLOG_TAG_FEED_TITLE = '%s - Entries tagged "%%(tag.name)s"' % BLOG_FEED_TITLE