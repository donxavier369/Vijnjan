
from rest_framework import serializers
from .models import Meetings
from accounts.models import CustomUser
from courses.models import Courses

class MeetingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(person = 'tutor'))
    class Meta:
        model = Meetings
        fields = ['id', 'date', 'time', 'am_pm', 'course', 'duration', 'tutor', 'link']

