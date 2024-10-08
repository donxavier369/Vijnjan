from rest_framework import serializers
from .models import Courses, Modules, Categories, Files
from django.core.validators import MinValueValidator
import os
from django.conf import settings
from .utils import convert_ppt_to_pdf  


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


# class CourseSerializer(serializers.ModelSerializer):
#     # category_name = serializers.SerializerMethodField()
#     tutor_name = serializers.SerializerMethodField()
#     tutor_id = serializers.SerializerMethodField()


#     # def get_category_name(self, obj):
#     #     return obj.category.category_name

#     def get_tutor_name(self, obj):
#         return obj.tutor.username  
    
#     def get_tutor_id(self, obj):
#         return obj.tutor.id

#     class Meta:
#         model = Courses
#         fields = ('id', 'name', 'description', 'thumbnail', 'duration', 'category', 'is_trending', 'tutor_name', 'tutor_id')

#         # Validate duration to be positive
#         extra_kwargs = {'duration': {'validators': [MinValueValidator(1)]}}

class CourseSerializer(serializers.ModelSerializer):
    tutor = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = ('id', 'name', 'description', 'thumbnail', 'duration', 'category', 'is_trending', 'tutor')

        # Validate duration to be positive
        extra_kwargs = {'duration': {'validators': [MinValueValidator(1)]}}

    def get_tutor(self, obj):
        request = self.context.get('request')
        tutor = obj.tutor
        tutor_data = {
            "id": tutor.id,
            "username": tutor.username,
            "email": tutor.email,
            "profile_image": self.get_profile_image(tutor, request),
            "person": tutor.person,
            "date_of_birth": tutor.date_of_birth,
            "gender": tutor.gender,
            "is_tutor_verify": tutor.is_tutor_verify
        }
        return tutor_data

    def get_profile_image(self, tutor, request):
        if tutor.profile_image:
            if request is not None:
                profile_image = request.build_absolute_uri(tutor.profile_image.url)
                if profile_image and not profile_image.startswith(('http://', 'https://')):
                    profile_image = 'https://' + profile_image
            else:
                profile_image = tutor.profile_image.url
            return profile_image
        return None

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files
#         fields = '__all__'

#     def create(self, validated_data):
#         print(self.context, "kkkkkkkkkkkk", validated_data)
#         ppt_file = self.context['request'].FILES['ppt']
#         print(ppt_file,"ppt fileeeeeee")
#         pdf_file = convert_ppt_to_pdf(ppt_file)  # Convert PPT to PDF
#         print(pdf_file,"pdfffffffffff")

#         # Save the PDF file to the model
#         validated_data['ppt'] = pdf_file
#         return super().create(validated_data)