from django.contrib.auth.models import User
from django.db import models

class RareUsers(models.Model):
    bio = models.CharField(max_length=2000)
    profile_image_url = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rare_username = models.CharField(max_length=64)