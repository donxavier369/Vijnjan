from .serializers import CourseSerializer, ModuleSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses


class CourseCreateAPIView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()

            course_id = course.id
            
            # Create associated modules
            request_modules = request.data.get('modules', [])
            for module_data in request_modules:
                module_data['course'] = course_id
                module_serializer = ModuleSerializer(data=module_data)
                if module_serializer.is_valid():
                    module_serializer.save(course=course)
                else:
                    raise serializers.ValidationError(module_serializer.errors)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            course = Courses.objects.get(pk=pk)
        except Courses.DoesNotExist:
            return Response({"error": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the course
        course.delete()
        
        return Response({"success": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ssh -i "don3.pem" ubuntu@ec2-54-157-52-2.compute-1.amazonaws.com