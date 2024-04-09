
from rest_framework import serializers
from .models import Meetings
from accounts.models import CustomUser
from courses.models import Courses

class MeetingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(is_tutor=True))
    class Meta:
        model = Meetings
        fields = ['id', 'date', 'time', 'course', 'duration', 'tutor', 'link']

