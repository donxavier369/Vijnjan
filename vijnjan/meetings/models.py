from django.db import models
from accounts.models import CustomUser
from courses.models import Courses
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


def validate_positive_duration(value):
    if value < 0:
        raise ValidationError(
            _("Duration must be positive value"),
            params={"value":value},
        )
    

class Meetings(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    # am_pm = models.CharField(max_length=2, choices=(("AM", "AM"), ("PM", "PM")), default="AM")
    duration = models.IntegerField(default=0, validators=[validate_positive_duration])
    link = models.CharField(max_length=255)