from rest_framework import serializers
from .models import Carousel
from courses.models import Courses
from .models import Notifications
from django.contrib.auth import authenticate
from accounts.models import CustomUser


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_image', 'is_superuser']
    
class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

class ListNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'notification']