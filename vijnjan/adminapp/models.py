from django.db import models

# Create your models here.

class Carouse(models.Model):
    carousel_image = models.FileField(upload_to='modules/carousel_image', null=True, blank=True)
