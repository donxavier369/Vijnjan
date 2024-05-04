from rest_framework import serializers
from .models import Courses, Modules, Categories, Files
from django.core.validators import MinValueValidator


class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Courses.objects.all())

    class Meta:
        model = Modules
        fields = '__all__'  # Include all fields


class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    tutor_name = serializers.SerializerMethodField()
    tutor_id = serializers.SerializerMethodField()


    def get_category_name(self, obj):
        return obj.category.category_name

    def get_tutor_name(self, obj):
        return obj.tutor.username  
    
    def get_tutor_id(self, obj):
        return obj.tutor.id

    class Meta:
        model = Courses
        fields = ('id', 'name', 'description', 'thumbnail', 'duration', 'category', 'category_name', 'tutor_name', 'tutor_id')

        # Validate duration to be positive
        extra_kwargs = {'duration': {'validators': [MinValueValidator(1)]}}

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'