from django.db import models

class PostTags(models.Model):
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)