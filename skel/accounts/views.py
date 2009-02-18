from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.models import User

def user_detail(request, user=None, **kwargs):
    """Wrapper for object_detail that takes username from url"""
    pk = User.objects.get(username=user).pk
    return object_detail(request, object_id=pk, **kwargs)