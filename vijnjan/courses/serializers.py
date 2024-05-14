from rest_framework import serializers
from .models import Courses, Modules, Categories, Files
from django.core.validators import MinValueValidator


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['course', 'module_name', 'module_type', 'module_content_ppt', 'module_content_video']

    def create(self, validated_data):
        course_instance = self.context.get('course_instance')  # Get course_instance from context
        
        # Remove 'course' key from validated_data
        validated_data.pop('course', None)
        
        module = Modules(course=course_instance, **validated_data)
        module.save()
        return module


class CourseSerializer(serializers.ModelSerializer):
    # category_name = serializers.SerializerMethodField()
    tutor_name = serializers.SerializerMethodField()
    tutor_id = serializers.SerializerMethodField()


    # def get_category_name(self, obj):
    #     return obj.category.category_name

    def get_tutor_name(self, obj):
        return obj.tutor.username  
    
    def get_tutor_id(self, obj):
        return obj.tutor.id

    class Meta:
        model = Courses
        fields = ('id', 'name', 'description', 'thumbnail', 'duration', 'category', 'is_trending', 'tutor_name', 'tutor_id')

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