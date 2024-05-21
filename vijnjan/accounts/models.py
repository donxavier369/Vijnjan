from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from PIL import Image
from django.core.exceptions import ValidationError

def validate_profile_image_size(value):
    img = Image.open(value)

    if value.size > 1000 * 1024:  
        raise ValidationError("Image file size cannot exceed 1MB.")


USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('tutor', 'Tutor'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    profile_image = models.ImageField(upload_to="profile/profile_image", validators=[validate_profile_image_size], null=True, blank=True, default=None)
    person = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    date_of_birth = models.DateField(default = date.today)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
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
