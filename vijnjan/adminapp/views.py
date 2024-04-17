from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carousel, Notifications
from .serializers import CarouselSerializer,ListNotificationSerializer
from django.shortcuts import get_object_or_404
from courses.models import Courses, Categories
from courses.serializers import CourseSerializer,CategorySerializer
from accounts.models import CustomUser

class CarouselUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CarouselSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"carousel successfully added","data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"unable to add carousel","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CarouselDeleteView(APIView):
    def delete(self, request, id):
        try:
            carousel = Carousel.objects.get(id=id)
            carousel.delete()
            return Response({"success":"carousel deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Carousel.DoesNotExist:
            return Response({"error":"carousel not found"}, status=status.HTTP_404_NOT_FOUND)


class CarouselListView(APIView):
    def get(self, request):
        try:
            carousels = Carousel.objects.all()
            serializer = CarouselSerializer(carousels, many=True)
            return Response({"success":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"error":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class TrendingCourseUpdateView(APIView):
    def post(self, request, course_id):
        try:
            course = Courses.objects.get(pk=course_id)
        except Courses.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the is_trending field based on the request data
        is_trending = request.data.get('is_trending', False)
        course.is_trending = is_trending
        course.save()

        # Serialize the updated course data
        serializer = CourseSerializer(course)
        return Response({"success":serializer.data}, status=status.HTTP_200_OK)
    

class ListNotification(APIView):
    def get(self, request):
        try:
            notifications = Notifications.objects.all().order_by('-id')  
            serializer = ListNotificationSerializer(notifications, many=True) 
            return Response({"success":serializer.data}, status=status.HTTP_200_OK)  
        except:
            return Response({"error":"internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class CreateCourseCategory(APIView):
     def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        try:
            # Check if the category already exists
            queryset = Categories.objects.filter(category_name=request.data['category_name'])
            if queryset.exists():
                return Response({"info": f"{request.data['category_name']} category already exists"})
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success": serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            # Handle the case when 'category_name' is not found in request data
            return Response({"error": "Category name not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any other unexpected exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class ListCourseCategory(APIView):
    def get(self, request):
        try:
            categories = Categories.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({"success":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"error":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteCourseCategory(APIView):
    def delete(self, request, category_id):
        try:
            category = Categories.objects.get(pk=category_id)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
        except Categories.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
            
class VerifyTutor(APIView):
    def patch(self,request, tutor_id):
        try:
            tutor = CustomUser.objects.get(id=tutor_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"Tutor not found"}, status=status.HTTP_404_NOT_FOUND)
        if not tutor.is_tutor:
            return Response({"error":"This user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif tutor.is_tutor_verify :
            return Response({"info":"This tutor is already verified"}, status=status.HTTP_200_OK)
        else:
            try:
                tutor.is_tutor_verify = True
                tutor.save()
                return Response({"success":"Tutor verified successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"error":"Unable to verify the tutor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        