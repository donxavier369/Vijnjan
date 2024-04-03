from rest_framework import serializers
from .models import Courses, Modules, Categories
from django.core.validators import MinValueValidator


class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Courses.objects.all())

    class Meta:
        model = Modules
        fields = '__all__'  # Include all fields


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = ('id', 'name', 'description', 'thumbnail', 'duration', 'tutor')

        # Validate duration to be positive
        extra_kwargs = {'duration': {'validators': [MinValueValidator(1)]}}

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = '__all__'