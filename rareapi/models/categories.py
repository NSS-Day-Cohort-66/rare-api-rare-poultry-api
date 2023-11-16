from django.db import models


class Categories(models.Model):
    label = models.CharField(max_length=155)