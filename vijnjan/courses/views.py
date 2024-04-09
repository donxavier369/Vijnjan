from .serializers import CourseSerializer, ModuleSerializer, CategorySerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses, Modules, Categories
from accounts.models import CustomUser,StudentProfile
from django.shortcuts import get_object_or_404



class CourseCreateAPIView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()

            # Create associated modules
            request_modules = request.data.get('modules', [])
            for module_data in request_modules:
                module_data['course'] = course.id
                module_serializer = ModuleSerializer(data=module_data)
                if module_serializer.is_valid():
                    module_serializer.save(course=course)
                else:
                    course.delete()  # Delete the created course if module creation fails
                    return Response({"error": "Failed to create module", "details": module_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": "Course created successfully", "course": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create course", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CourseDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            course = Courses.objects.get(pk=pk)
            course.delete()
            return Response({"success": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Courses.DoesNotExist:
            return Response({"error": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Failed to delete course: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseListAPIView(APIView):
    def get(self, request):
        try:
            courses = Courses.objects.all()

            if not courses:
                return Response({
                    "success": True,
                    "message": "No courses found",
                    "courses": []
                }, status=status.HTTP_200_OK)
            else:
                serializer = CourseSerializer(courses, many=True)
                return Response({
                    "success": True,
                    "message": "Courses fetched successfully",
                    "courses": serializer.data
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch courses: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleListAPIView(APIView):
    def get(self, request, course_id, user_id):
        try:
            course = Courses.objects.get(id=course_id)
            user = CustomUser.objects.get(id=user_id)

            # Check if the user is enrolled in the course
            if not StudentProfile.objects.filter(student=user, courses=course).exists():
                # If not enrolled, enroll the user in the course
                StudentProfile.objects.create(student=user, courses=course)

            modules = Modules.objects.filter(course=course)

            if not modules:
                return Response({
                    "success": True,
                    "message": "No modules found for this course",
                    "modules": []
                }, status=status.HTTP_200_OK)
            else:
                serializer = ModuleSerializer(modules, many=True)
                return Response({
                    "success": True,
                    "message": "Modules fetched successfully",
                    "modules": serializer.data
                }, status=status.HTTP_200_OK)
        except Courses.DoesNotExist:
            return Response({
                "success": False,
                "message": "Course does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch modules: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TrendingCourseListAPIView(APIView):
    def get(self, request):
        try:
            courses = Courses.objects.filter(is_trending=True)

            if not courses:
                return Response({
                    "success": True,
                    "message": "No trending courses found",
                    "courses": []
                }, status=status.HTTP_200_OK)
            else:
                serializer = CourseSerializer(courses, many=True)
                return Response({
                    "success": True,
                    "message": "Trending courses fetched successfully",
                    "courses": serializer.data
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch trending courses: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryCourseListView(APIView):
    def get(self, request):
        try:
            categories = Categories.objects.all()
            course_data = []

            for category in categories:
                courses = Courses.objects.filter(category=category)
                serializer_courses = CourseSerializer(courses, many=True).data
                serializer_category = CategorySerializer(category).data
                
                course_data.append({
                    'category': serializer_category,
                    'courses': serializer_courses
                })

            return Response({
                'success': True,
                'message': 'Categories and courses fetched successfully',
                'data': course_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Failed to fetch categories and courses: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)