from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField(blank=True, verify_exists=True)
    bio = models.TextField(blank=True)