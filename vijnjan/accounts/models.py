from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_tutor = models.BooleanField(default = False)
    date_of_birth = models.DateField(default = date.today)
    gender = models.CharField(max_length=10, default = '')


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username
