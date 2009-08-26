from skel.core.sitemaps import GenericSitemap
from skel.blog.models import Entry

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'updated',
}

EntrySitemap = GenericSitemap(info_dict, priority=0.6)