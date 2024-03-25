from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carousel
from .serializers import CarouselSerializer
from django.shortcuts import get_object_or_404
from courses.models import Courses
from courses.serializers import CourseSerializer


class CarouselUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CarouselSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarouselDeleteView(APIView):
    def delete(self, request, id):
        carousel = get_object_or_404(Carousel, id=id)
        carousel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarouselListView(APIView):
    def get(self, request):
        carousels = Carousel.objects.all()
        serializer = CarouselSerializer(carousels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TrendingCourseUpdateView(APIView):
    def post(self, request, course_id):
        try:
            course = Courses.objects.get(pk=course_id)
        except Courses.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the is_trending field based on the request data
        is_trending = request.data.get('is_trending', False)
        course.is_trending = is_trending
        course.save()

        # Serialize the updated course data
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)