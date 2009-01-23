from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail

info_dict = {
    'queryset': User.objects.all(),
}

def user_view(*args, **kwargs):
    pk = User.objects.get(username=kwargs.pop('user')).pk
    return object_detail(object_id=pk, *args, **kwargs)

urlpatterns = patterns('',
    url(
        r'^/?$',
        object_list,
        info_dict,
        name='user-list'
    ),

    url(r'^(?P<user>.*)/$',
        user_view,
        info_dict,
        name='user-detail'
    ),
)