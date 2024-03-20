from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Meatings(models.Model):
    meating_name = models.CharField(max_length=50)
    content = models.CharField(max_length=255)  
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    time = models.DateTimeField()
    link = models.CharField(max_length=255)