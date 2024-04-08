from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    profile_image = models.ImageField(upload_to="profile/profile_image", null=True, blank=True, default=None)
    is_tutor = models.BooleanField(default = False)
    date_of_birth = models.DateField(default = date.today)
    gender = models.CharField(max_length=10, default = '')
    is_tutor_verify = models.BooleanField(default=False)

    


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username
    
class TutorProfile(models.Model):
    tutor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100, default='')
    certificate = models.FileField(upload_to='tutorprofile/pdf')


class StudentProfile(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    courses = models.ForeignKey('courses.Courses', on_delete=models.CASCADE)
