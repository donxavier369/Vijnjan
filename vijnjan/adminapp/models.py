from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError

# Create your models here.

def validate_carousel_image_size(value):
    img = Image.open(value)

    if value.size > 1000 * 1024:  
        raise ValidationError("Image file size cannot exceed 1MB.")

class Carousel(models.Model):
    carousel_image = models.FileField(upload_to='carousel_image', validators=[validate_carousel_image_size], null=False, blank=False)

class Notifications(models.Model):
    notification = models.CharField(max_length=255) 