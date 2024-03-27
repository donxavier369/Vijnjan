from rest_framework import serializers
from .models import Carousel
from courses.models import Courses
from .models import Notifications

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

class ListNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'notification']