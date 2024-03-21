from django.db import models

# Create your models here.



class Courses(models.Model):
    name = models.CharField(max_length=50)

class Modules(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=50)
    module_content = models.CharField(max_length=255)


    