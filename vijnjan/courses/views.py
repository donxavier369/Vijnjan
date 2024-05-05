from .serializers import CourseSerializer, ModuleSerializer, CategorySerializer, FileSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses, Modules, Categories, Files
from accounts.models import CustomUser,StudentProfile
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import MODULE_TYPE_CHOICES
from django.db import transaction
import json
from rest_framework.exceptions import AuthenticationFailed




class AddVideoPptAPI(APIView):
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        # tutor_id = request.user.id
        # tutor_from_data = request.data.get('tutor')
        # print(tutor_from_data,"datttttttttt", tutor_id)
        # if tutor_from_data is None:
        #      return Response({"success": False, "message": "Tutor ID is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
        # if tutor_id != int(tutor_from_data):
        #     return Response({"success": False, "message":"Authentication credential and given tutor id do not match"}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     tutor = CustomUser.objects.get(id=tutor_id)
        # except CustomUser.DoesNotExist:
        #     return Response({"success": False,"message": "Tutor does not exists", "data": serializer.data}, status=status.HTTP_404_NOT_FOUND)
        # if tutor.person != 'tutor':
        #     return Response({"success":False,"message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        # elif tutor.is_tutor_verify !=True:
        #     return Response({"success":True,"message": "The tutor not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(): 
            serializer.save()
            return Response({"success": True,"message": "files added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message":"fail to add files", "error": serializer.errors})

class GetFiles(APIView):
    def get(self, request, tutor_id):
        try:
            tutor = CustomUser.objects.get(id=tutor_id)
        except CustomUser.DoesNotExist:
            return Response({"success": False,"message": "Tutor does not exists", "data": serializer.data}, status=status.HTTP_404_NOT_FOUND)
        if tutor.person != 'tutor':
            return Response({"success":False,"message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif tutor.is_tutor_verify !=True:
            return Response({"success":True,"message": "The tutor not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            files = Files.objects.filter(tutor=tutor_id)
            serializer = FileSerializer(instance=files, many=True)  
            return Response({"success": True,"message":"files fetched successfully", "data": serializer.data})
   
    
class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user.id)
        print(request.data)
        serializer = CourseSerializer(data=request.data)
        try:
            tutor = CustomUser.objects.get(id=request.user.id)
        except:
            return Response({'success':False,'message':'Tutor not found'}, status=status.HTTP_404_NOT_FOUND)
        if tutor.person != 'tutor':
            return Response({"success":False,"message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif tutor.is_tutor_verify !=True:
            return Response({"success":True,"message": "The tutor not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                course = serializer.save(tutor=tutor)
                

                return Response({"success":True,"message": "Course created successfully", "course": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success":False,"message": "Failed to create course", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    
class AddModulesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ModuleSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, "message": "Module added successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": "Unable to add modules", "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# class ModuelCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = ModuleSerializer(data=request.data)
#         module_type = request.data.get('module_type')
#         get_course = request.data.get('course')
#         module_content_video = request.data.get('module_content_video')
#         module_content_ppt = request.data.get('module_content_ppt')
#         tutor_id = request.user.id

#         if module_content_ppt is None and module_content_video is None:
#             return Response({"success": False, "message": "module_content_video or module_content_ppt is required to add a module"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             course = Courses.objects.get(id=get_course)
#         except Courses.DoesNotExist:
#             return Response({"success": False, "message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#         if tutor_id != course.tutor.id:
#             return Response({"success": False, "message": "Provided course does not belong to the tutor"}, status=status.HTTP_400_BAD_REQUEST)
            
#         if module_type not in dict(MODULE_TYPE_CHOICES).keys():
#             return Response({"success": False, "message": "Invalid choice for module type. Valid choices are: video, ppt"}, status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": True, "message": "Module added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"success": False, "message": "Failed to add module", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   

class CourseDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({"success": False, "message": "Admin does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not admin.is_superuser:
            return Response({"success": False, "message": "Provided user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Courses.objects.get(pk=pk)
            course.delete()
            return Response({"success": True, "message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Courses.DoesNotExist:
            return Response({"success": False, "message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({"success": False, "message": f"Token is invalid or expired: {str(e.detail)}"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False, "message": f"Failed to delete course: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
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
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        print(request.user.id)
        try:
            course = Courses.objects.get(id=course_id)
            user = CustomUser.objects.get(id=request.user.id)

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