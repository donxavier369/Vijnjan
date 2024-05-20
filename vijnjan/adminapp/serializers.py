from rest_framework import serializers
from .models import Carousel
from courses.models import Courses
from .models import Notifications
from django.contrib.auth import authenticate
from accounts.models import CustomUser


class AdminSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_image', 'is_superuser']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    
class CarouselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

class CarouselListSerializer(serializers.ModelSerializer):
    carousel_image = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

    def get_carousel_image(self, obj):
        request = self.context.get('request')
        if obj.carousel_image:
            return request.build_absolute_uri(obj.carousel_image.url)
        return None

    carousel_image = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

    def get_carousel_image(self, obj):
        request = self.context.get('request')
        if obj.carousel_image:
            return request.build_absolute_uri(obj.carousel_image.url)
        return None

class ListNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'notification']