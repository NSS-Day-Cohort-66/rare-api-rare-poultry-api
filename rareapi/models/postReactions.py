from django.db import models
from django.contrib.auth.models import User

class PostReactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    reaction = models.ForeignKey('Reactions', on_delete=models.CASCADE)
    
