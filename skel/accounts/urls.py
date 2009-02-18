from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list
from skel.accounts.views import user_view

info_dict = {
    'queryset': User.objects.all(),
}

urlpatterns = patterns('',
    url(
        r'^/?$',
        object_list,
        dict(info_dict, template_name='accounts/user_list.html'),
        name='user-list'
    ),

    url(r'^(?P<user>.*)/$',
        user_view,
        dict(info_dict, template_name='accounts/user_detail.html'),
        name='user-detail'
    ),
)