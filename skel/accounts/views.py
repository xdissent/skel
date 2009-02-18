from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.models import User

def user_view(*args, **kwargs):
    """Wrapper for object_detail that takes username from url"""
    pk = User.objects.get(username=kwargs.pop('user')).pk
    return object_detail(object_id=pk, *args, **kwargs)