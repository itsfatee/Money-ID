from django.db import models

# Create your models here.
class Image(models.Model):
    image_to_detect = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)