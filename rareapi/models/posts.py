from django.db import models

class Posts(models.Model):
    title = models.CharField(max_length=250)
    publication_date = models.DateField()
    image_url = models.URLField(max.length=1100, blank=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    category = models.ForeignKey('Categories')


