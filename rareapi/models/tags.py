from django.db import models

class Tags(models.Model):
    label = models.CharField(max_length=64)