from rest_framework import serializers
from .models import Courses, Modules

class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['id', 'course', 'module_name', 'module_content']

class CoursesSerializer(serializers.ModelSerializer):
    modules = ModulesSerializer(many=True, read_only=True)

    class Meta:
        model = Courses
        fields = ['id', 'name', 'modules']

