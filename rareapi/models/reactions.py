from django.db import models

class Reactions(models.Model):
    label = models.CharField(max_length=200)
    image_url = models.URLField(null=True, blank=True)
    