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
            profile_image= request.build_absolute_uri(obj.profile_image.url)
            if profile_image is not None:
                if profile_image.startswith('http://'):
                    profile_image = profile_image.replace('http://', 'https://')
                elif not profile_image.startswith('https://'):
                    profile_image = 'https://' + profile_image
            return profile_image
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
            carousel_images= request.build_absolute_uri(obj.carousel_image.url)
            if carousel_images is not None:
                if carousel_images.startswith('http://'):
                    carousel_images = carousel_images.replace('http://', 'https://')
                elif not carousel_images.startswith('https://'):
                    carousel_images = 'https://' + carousel_images
            return carousel_images
        return None

    carousel_image = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

    def get_carousel_image(self, obj):
        request = self.context.get('request')
        if obj.carousel_image:
            carousel_images= request.build_absolute_uri(obj.carousel_image.url)
            if carousel_images is not None:
                if carousel_images.startswith('http://'):
                    carousel_images = carousel_images.replace('http://', 'https://')
                elif not carousel_images.startswith('https://'):
                    carousel_images = 'https://' + carousel_images
            return carousel_images
        return None

class ListNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'notification']