from django.conf import settings

SKEL_BLOG_MARKUP_ENABLED = ('skel.markup' in settings.INSTALLED_APPS)

SKEL_BLOG_MEDIA_ENABLED = ('massmedia' in settings.INSTALLED_APPS)

SKEL_BLOG_TAGGING_ENABLED = ('tagging' in settings.INSTALLED_APPS)

SKEL_BLOG_CATEGORIES_ENABLED = ('skel.categories' in settings.INSTALLED_APPS)

SKEL_BLOG_COMMENTS_ENABLED = ('django.contrib.comments' in settings.INSTALLED_APPS)

SKEL_BLOG_AUTO_CLOSE_COMMENTS_DAYS = 60

SKEL_BLOG_FEEDS_ENABLED = True

SKEL_BLOG_FEED_TITLE = 'Skel Blog Feed'

SKEL_BLOG_FEED_DESCRIPTION = 'Skel Blog Feed'

SKEL_BLOG_FEED_NUM_ITEMS = 10

SKEL_BLOG_FEED_SHOW_AUTHOR_EMAIL = False

# These have undesired effects
# SKEL_BLOG_CATEGORY_FEED_TITLE = '%s - %%(category.title)s Category' % SKEL_BLOG_FEED_TITLE
# SKEL_BLOG_TAG_FEED_TITLE = '%s - Entries tagged "%%(tag.name)s"' % SKEL_BLOG_FEED_TITLE
SKEL_BLOG_CATEGORY_FEED_TITLE = '%s Category'
SKEL_BLOG_TAG_FEED_TITLE = 'Entries tagged "%s"'