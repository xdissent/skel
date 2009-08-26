from django.conf import settings

# Determine whether or not to accept marked up comments.
SKEL_COMMENTS_MARKUP = ('django.contrib.comments' in settings.INSTALLED_APPS and
                        'skel.markup' in settings.INSTALLED_APPS)

# If ``SKEL_COMMENTS_ENABLED_DEFAULT`` is a boolean value, commenting will be
# enabled (True) or disabled (False) by default for all models. If a tuple 
# of model names in the form ``app.model`` are provided, those models will
# have comments enabled by default while all others will not.
SKEL_COMMENTS_ENABLED_DEFAULT = True