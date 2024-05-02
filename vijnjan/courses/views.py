from .serializers import CourseSerializer, ModuleSerializer, CategorySerializer, FileSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses, Modules, Categories, Files
from accounts.models import CustomUser,StudentProfile
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class AddVideoPptAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        tutor_id = request.user.id
        tutor_from_data = request.data.get('tutor')
        print(tutor_from_data,"datttttttttt", tutor_id)
        if tutor_from_data is None:
             return Response({"success": False, "message": "Tutor ID is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
        if tutor_id != int(tutor_from_data):
            return Response({"success": False, "message":"Authentication credential and given tutor id do not match"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tutor = CustomUser.objects.get(id=tutor_id)
        except CustomUser.DoesNotExist:
            return Response({"success": False,"message": "Tutor does not exists", "data": serializer.data}, status=status.HTTP_404_NOT_FOUND)
        if tutor.person != 'tutor':
            return Response({"success":False,"message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif tutor.is_tutor_verify !=True:
            return Response({"success":True,"message": "The tutor not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
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
   

class SampleCourseCreateAPIView(APIView):
    def post(self, request):
        print(request.user.id)
        print(request.data)

        


            # Create associated modules
        request_modules = request.data.get('modules', [])
        print(request_modules, "requestttttttttttttted data")
        for module_data in request_modules:
            print(module_data,"mmmmmmmmmmmmmm")
        return Response({"success":True,"message": "Course created successfully"}, status=status.HTTP_201_CREATED)


    
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

                # Create associated modules
                request_modules = request.data.get('modules', [])
                # request_modules = request.data.getlist('modules')
                print(request_modules)
                for module_data in request_modules:
                    print(module_data,"mmmmmmmmmmmmmm")
                    module_data['course'] = course.id
                    module_serializer = ModuleSerializer(data=module_data)
                    if module_serializer.is_valid():
                        module_serializer.save(course=course)
                    else:
                        course.delete()  # Delete the created course if module creation fails
                        return Response({"success":False,"message": "Failed to create module", "details": module_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"success":True,"message": "Course created successfully", "course": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success":False,"message": "Failed to create course", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CourseDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            course = Courses.objects.get(pk=pk)
            course.delete()
            return Response({"success":True,"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Courses.DoesNotExist:
            return Response({"success":False,"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":True,"message": f"Failed to delete course: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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