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
from collections import defaultdict
from django.core.files.storage import FileSystemStorage
import os
from django.http import HttpResponse
import subprocess
from django.db.models import Q




class AddVideoPptAPI(APIView):
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            ppt_file = request.FILES.get('ppt')
            pdf_url = None
            
            # Check if ppt_file is provided and valid
            if ppt_file:
                valid_extensions = ['ppt', 'pptx']
                if not ppt_file.name.lower().endswith(tuple(valid_extensions)):
                    return Response({"success": False, "message": "Invalid file format. Only PPT and PPTX files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
                
            fs = FileSystemStorage()
            
            # Save the ppt file if provided
            if ppt_file:
                filename = fs.save(ppt_file.name, ppt_file)
                uploaded_file_path = fs.path(filename)

                pdf_filename = f"{os.path.splitext(filename)[0]}.pdf"
                pdf_file_path = os.path.join(fs.location, pdf_filename)

                try:
                    # Convert PPT to PDF using LibreOffice
                    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', uploaded_file_path, '--outdir', fs.location], check=True)

                    # Get the URL of the PDF file
                    pdf_url = fs.url(pdf_filename)
                    
                    # Set the ppt file URL to pdf_url
                    ppt_url = pdf_url
                except subprocess.CalledProcessError as e:
                    return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                ppt_url = None

            # Create the file instance
            file_instance = serializer.save(ppt=ppt_url)
            
            # Build the full URL for the video file
            video_url = request.build_absolute_uri(file_instance.video.url) if file_instance.video else None
            if video_url is not None:
                if video_url.startswith('http://'):
                    video_url = video_url.replace('http://', 'https://')
                elif not video_url.startswith('https://'):
                    video_url = 'https://' + video_url

            thumbnail_url = request.build_absolute_uri(file_instance.thumbnail.url) if file_instance.thumbnail else None
            if thumbnail_url is not None:
                if thumbnail_url.startswith('http://'):
                    thumbnail_url = thumbnail_url.replace('http://', 'https://')
                elif not thumbnail_url.startswith('https://'):
                    thumbnail_url = 'https://' + thumbnail_url
            
            pdf_url =request.build_absolute_uri(pdf_url) if pdf_url else None
            if pdf_url is not None:
                if pdf_url.startswith('http://'):
                    pdf_url = pdf_url.replace('http://', 'https://')
                elif not pdf_url.startswith('https://'):
                    pdf_url = 'https://' + pdf_url
            response_data = {
                
                "id": file_instance.id,
                "thumbnail": thumbnail_url,
                "video": video_url,
                "pdf": pdf_url
               
            }
            return Response({"success": True, "message": "File added successfully", "data":response_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "Failed to add files", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class GetFiles(APIView):
    def get(self, request):
        files = Files.objects.all()
        serializer = FileSerializer(instance=files, many=True)  
        return Response({"success": True,"message":"files fetched successfully", "data": serializer.data})

class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_data = request.data.copy()
        modules_data = course_data.pop('modules', [])
        try:
            tutor = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success': False, 'message': 'Tutor not found'}, status=status.HTTP_404_NOT_FOUND)
        if tutor.person != 'tutor':
            return Response({"success": False, "message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif not tutor.is_tutor_verify:
            return Response({"success": False, "message": "The tutor is not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            course_serializer = CourseSerializer(data=course_data)
            response_module = []
            if course_serializer.is_valid():
                course_instance = course_serializer.save(tutor=tutor)

                for module_data in modules_data:
                    module_data['course'] = course_instance.id  # Update validated_data
                    module_serializer = ModuleSerializer(data=module_data, context={'course_instance': course_instance})
                    if module_serializer.is_valid():
                        module_serializer.save()
                        response_module.append(module_data)
                    else:
                        # If module data is not valid, delete the created course instance
                        course_instance.delete()
                        return Response({"success": False, "message": "Module data is not valid", "error": module_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
                return Response({"success": True, 
                                 "message": "Course created successfully", 
                                 "course_data": course_serializer.data,
                                 "module_data": response_module
                                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "message": "Course data is not valid", "error": course_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CourseSearchAPIView(APIView):
    def get(self, request):
        query = request.data.get('search', '')
        print(query)
        if query:
            courses = Courses.objects.filter(Q(name__icontains=query))
            serializer = CourseSerializer(courses, many=True)
            return Response({"success": True, "message": "Courses listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)

# class CourseDeleteAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             admin = CustomUser.objects.get(id=request.user.id)
#         except CustomUser.DoesNotExist:
#             return Response({"success": False, "message": "Admin does not exist"}, status=status.HTTP_400_BAD_REQUEST)

#         if not admin.is_superuser:
#             return Response({"success": False, "message": "Provided user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             course = Courses.objects.get(pk=pk)
#             thumbnail_url = course.thumbnail

#             # Remove base URL to get the relative path
#             base_url = 'http://127.0.0.1:8000/media/'
#             relative_thumbnail_path = thumbnail_url.replace(base_url, '')

#             # Delete the corresponding file in the Files model
#             file_thumbnail = Files.objects.filter(thumbnail=relative_thumbnail_path)
#             file_thumbnail.delete()

#             modules = Modules.objects.filter(course=course.id)
#             for module in modules:
#                 if module.module_content_video:
#                     video_path = module.module_content_video.replace(base_url, '')
#                     file_video = Files.objects.filter(video = video_path)
#                     file_video.delete()
#                 if module.module_content_ppt:
#                     base_url_pdf = 'http://127.0.0.1:8000'
#                     pdf_path = module.module_content_ppt.replace(base_url_pdf, '')
#                     file_ppt = Files.objects.filter(ppt = pdf_path)
#                     file_ppt.delete()
                
                
#             module.delete()
#             course.delete()
#             return Response({"success": True, "message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         except Courses.DoesNotExist:
#             return Response({"success": False, "message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
#         except AuthenticationFailed as e:
#             return Response({"success": False, "message": f"Token is invalid or expired: {str(e.detail)}"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({"success": False, "message": f"Failed to delete course: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({"success": False, "message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Courses.objects.get(pk=pk)
        except Courses.DoesNotExist:
            return Response({"success": False, "message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.is_superuser and user.person != 'tutor':
            return Response({"success": False, "message": "User is not authorized to delete this course"}, status=status.HTTP_403_FORBIDDEN)

        print(course.tutor.id, "lllllll", user.id)
        if course.tutor.id != user.id :
            return Response({"success": False, "message":"This course is not created by the tutor"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            thumbnail_url = course.thumbnail

            # Remove base URL to get the relative path
            base_url = 'http://127.0.0.1:8000/media/'
            relative_thumbnail_path = thumbnail_url.replace(base_url, '')

            # Delete the corresponding file in the Files model
            file_thumbnail = Files.objects.filter(thumbnail=relative_thumbnail_path)
            file_thumbnail.delete()

            modules = Modules.objects.filter(course=course.id)
            for module in modules:
                if module.module_content_video:
                    video_path = module.module_content_video.replace(base_url, '')
                    file_video = Files.objects.filter(video=video_path)
                    file_video.delete()
                if module.module_content_ppt:
                    base_url_pdf = 'http://127.0.0.1:8000'
                    pdf_path = module.module_content_ppt.replace(base_url_pdf, '')
                    file_ppt = Files.objects.filter(ppt=pdf_path)
                    file_ppt.delete()

                module.delete()

            course.delete()
            return Response({"success": True, "message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
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
                # Group courses by category
                courses_by_category = defaultdict(list)
                for course in courses:
                    category_name = course.category.category_name
                    serializer = CourseSerializer(course)
                    courses_by_category[category_name].append(serializer.data)
                
                # Include categories with no courses
                all_categories = Categories.objects.all()
                response_data = []
                for category in all_categories:
                    category_name = category.category_name
                    response_data.append({
                        "name": category_name,
                        "data": courses_by_category.get(category_name, [])
                    })

                return Response({
                    "success": True,
                    "message": "Courses fetched successfully",
                    "courses": response_data
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