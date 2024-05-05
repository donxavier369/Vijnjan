from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=100)

def validate_thumbnail_size(value):
    # Opening the image
    img = Image.open(value)

    # Checking the file size
    if value.size > 1000 * 1024:  
        raise ValidationError("Image file size cannot exceed 1MB.")

class Courses(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default="description")
    thumbnail = models.ImageField(upload_to='courses/thumbnail', validators=[validate_thumbnail_size])
    duration = models.IntegerField(default=1)
    tutor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_trending = models.BooleanField(default=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    

MODULE_TYPE_CHOICES = [
    ('video', 'Video'),
    ('ppt', 'ppt'),
]
class Modules(models.Model):
    course = models.ForeignKey('courses.Courses', on_delete=models.CASCADE)
    module_name = models.CharField(max_length=50)
    module_type = models.CharField(choices=MODULE_TYPE_CHOICES, default='ppt')
    module_content_ppt = models.FileField(upload_to='modules/ppt', null=True, blank=True)
    module_content_video = models.FileField(upload_to='modules/video', null=True, blank=True)
    

class Files(models.Model):
    ppt = models.FileField(upload_to='modules/ppt', null=True, blank=True)
    video = models.FileField(upload_to='modules/video', null=True, blank=True)
