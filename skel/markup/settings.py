# SKEL_MARKUP_ENGINES
# -------------------
# A dict of lists of markup engines to use for a particular model. The dict 
# keys should be in ``app.model:field`` format, where the model and source 
# field name are optional. An empty dict key indicates the default set of 
# engines to use if a more specific rule isn't found. Engine sets are *not*
# inherited from parent rules, and the most specific rule is matched first.
# 
# Example limiting markup choices for the ``content`` field of all 
# ``blog.entry`` instances, but allows only plain text processing for
# the rest of the fields in the ``blog.entry`` model:
#     SKEL_MARKUP_ENGINES = {
#         '': [
#             'text',
#             'markdown',
#             'rest',
#             'xhtml',
#         ],
#         'blog.entry:content': [
#             'rest',
#             'markdown',
#         ],
#     }

SKEL_MARKUP_ENGINES = {
    '': [
        'text',
        'markdown',
        'rest',
        'xhtml',
    ],
}



# SKEL_MARKUP_ENGINE_OPTIONS
# --------------------------
# A nested dict of options to use when rendering a marked up item.
# The markup engine created for each marked up item will parse this
# setting to determine which options to use when rendering. The dict uses
# the same format as ``SKEL_MARKUP_ENGINES``, and the final options
# are calculated in the same non-inherited fashion.
#
# Example adding the ``highlight`` option to the ``markdown`` engine
# for the ``content`` field of the ``blog.entry`` model.
#     SKEL_MARKUP_ENGINE_OPTIONS = {
#         '': {
#             'rest': {
#                 'doctitle_xform': False,
#                 'initial_header_level': '2',
#                 'cloak_email_addresses': True,
#             },
#             'markdown': {
#                 'footnotes': True,
#             }
#         },
#         'blog.entry:content': {
#             'markdown': {
#                 'highlight': True,
#             },
#         },
#     }
# Note that the settings for the ``rest`` engine *will* be inherited,
# but the settings for ``markdown`` will be completely overwritten, losing
# the ``footnotes`` default option.

SKEL_MARKUP_ENGINE_OPTIONS = {
    '': {
        'rest': {
            'doctitle_xform': False,
            'initial_header_level': '2',
            'cloak_email_addresses': True,
        },
    },
}


# SKEL_MARKUP_MODEL_FIELDS
# ------------------------
# A dict specifying which fields in a model should be handled by the markup 
# system. Keys in the dict should be in ``app.model`` and the value should
# be a list of fields to markup. If no key exists for a model being 
# registered, all ``django.db.models.TextField`` (or subclassed) fields 
# will be used.
# 
# Example which only uses the ``content`` field of the ``blog.entry`` model:
#     SKEL_MARKUP_MODEL_FIELDS = {
#         'blog.entry': ['content'],
#     }

SKEL_MARKUP_MODEL_FIELDS = {}