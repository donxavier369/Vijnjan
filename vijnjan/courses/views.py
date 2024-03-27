from .serializers import CourseSerializer, ModuleSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses, Modules
from accounts.models import CustomUser,StudentProfile


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


class CourseListAPIView(APIView):
    def get(self, request):
        try:
            courses = Courses.objects.all()

            if not courses:
                return Response({"courses": []}, status=status.HTTP_200_OK)
            else:
                serializer = CourseSerializer(courses, many=True)
                return Response({"courses": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleListAPIView(APIView):
    def get(self, request, course_id, user_id): 
        
        course = Courses.objects.get(id=course_id)
        user = CustomUser.objects.get(id=user_id)
        try:
            filter_course = StudentProfile.objects.get(student=user, courses=course)
        except:
            student = StudentProfile.objects.create(student=user, courses=course) 
        
        try:
            modules = Modules.objects.filter(course=course_id)

            if not modules:
                return Response({"modules": []}, status=status.HTTP_200_OK)
            else:
                # Using ModuleSerializer to serialize the queryset
                serializer = ModuleSerializer(modules, many=True)
                return Response({"modules": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TrendingCourseListAPIView(APIView):
    def get(self, request):
        try:
            courses = Courses.objects.filter(is_trending = True)

            if not courses:
                return Response({"courses": []}, status=status.HTTP_200_OK)
            else:
                serializer = CourseSerializer(courses, many=True)
                return Response({"courses": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












# ssh -i "don3.pem" ubuntu@ec2-54-157-52-2.compute-1.amazonaws.com
# 54.157.52.2
# https://documenter.getpostman.com/view/30403691/2sA35A7QNs#b9c42c3b-02c6-4971-b381-d7f0997c98ca