from rest_framework import serializers
from .models import Carouse

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carouse
        fields = ['id', 'carousel_image']