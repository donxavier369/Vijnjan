from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Courses
from .serializer import ModulesSerializer, CoursesSerializer

class CoursesCreateAPIView(APIView):
    """
    Create a new course.
    """
    def post(self, request, format=None):
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CoursesUpdateAPIView(APIView):
    """
    Update a course.
    """
    def put(self, request, pk, format=None):
        try:
            course = Courses.objects.get(pk=pk)
        except Courses.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoursesDeleteAPIView(APIView):
    """
    Delete a course.
    """
    def delete(self, request, pk, format=None):
        try:
            course = Courses.objects.get(pk=pk)
        except Courses.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({"message": "Course deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    
# ssh -i "don3.pem" ubuntu@ec2-54-157-52-2.compute-1.amazonaws.com
# http://54.157.52.2/