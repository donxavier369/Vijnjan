from django.db import models
from accounts.models import CustomUser
from courses.models import Courses
from django.utils import timezone


# Create your models here.

class Meetings(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    duration = models.IntegerField(default=0)
    link = models.CharField(max_length=255)