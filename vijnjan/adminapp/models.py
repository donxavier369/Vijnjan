from django.db import models

# Create your models here.

class Carousel(models.Model):
    carousel_image = models.FileField(upload_to='carousel_image')

class Notifications(models.Model):
    notification = models.CharField(max_length=255) 