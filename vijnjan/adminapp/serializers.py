from rest_framework import serializers
from .models import Carousel
from courses.models import Courses

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['id', 'carousel_image']

# class TrendingCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['id', 'iis_trending']