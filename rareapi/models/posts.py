from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    title = models.CharField(max_length=250)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    content = models.CharField(max_length=3000)
    tags = models.ManyToManyField('Tags', through='PostTags', related_name='posts')
