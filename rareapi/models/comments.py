from django.db import models

class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('RareUsers', on_delete=models.CASCADE, related_name='author')
    content = models.CharField(max_length=3000)
    created_on = models.DateField(auto_now_add=True)