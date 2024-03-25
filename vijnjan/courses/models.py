from django.db import models
# Create your models here.

class Courses(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default="description")
    duration = models.IntegerField(default=1)
    tutor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)



class Modules(models.Model):
    course = models.ForeignKey('courses.Courses', on_delete=models.CASCADE)
    module_name = models.CharField(max_length=50)
    module_type = models.CharField(max_length=50)
    module_content_ppt = models.FileField(upload_to='modules/ppt', null=True, blank=True)
    module_content_video = models.FileField(upload_to='modules/video', null=True, blank=True)
    


    