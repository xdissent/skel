from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list
from skel.accounts.views import user_detail

info_dict = {
    'queryset': User.objects.all(),
}

urlpatterns = patterns('',
    url(
        r'^/?$',
        object_list,
        dict(info_dict, template_name='accounts/users.html', paginate_by=10),
        name='users'
    ),

    url(r'^(?P<username>\w+)/$',
        user_detail,
        dict(info_dict, template_name='accounts/user.html'),
        name='user'
    ),
)


core_urlpatterns = patterns('',
    url(r'^users/', include((urlpatterns, 'accounts', 'accounts'))),
)