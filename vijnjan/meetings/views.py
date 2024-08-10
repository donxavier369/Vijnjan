from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Meetings
from .serializers import MeetingSerializer
from rest_framework import status
from courses.models import Courses
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser

# Create your views here.


class GenerateMeetingLink(APIView):
    def get(self, request):
        try:
            meeting_link = "https://meet.jit.si/" + get_random_string(length=10)
            return Response({"success":True,"message": "Meeting link generated successfully", "link": meeting_link}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success":False,"message": f"Failed to generate meeting link: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeetingApiView(APIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        meeting_data = request.data
        serializer = self.serializer_class(data=meeting_data)
        
        try:
            tutor = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({"success":False,"message": "Tutor not found"},status=status.http_404_not_found)
        if tutor.person != 'tutor':
            return Response({"success":False,"message": "Given user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
        elif tutor.is_tutor_verify !=True:
            return Response({"success":False,"error": "The tutor not verified by admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response({"success":True,"message": "Meeting created successfully","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success":False,"message": "Unable to create meeting", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MeetingListView(APIView):
    def get(self, request, course_id):
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({"success": False, "message": "Course does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        meetings = Meetings.objects.filter(course=course)
        serializer = MeetingSerializer(instance=meetings, many=True)  
        
        return Response({"success": True, "message": "Meetings listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
