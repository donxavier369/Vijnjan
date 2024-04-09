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
            meeting_link = "https://fanzkart.shop/" + get_random_string(length=10)
            return Response({"success": "Meeting link generated successfully", "link": meeting_link}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to generate meeting link: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeetingApiView(APIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        meeting_data = request.data
        serializer = self.serializer_class(data=meeting_data)
        user = get_object_or_404(CustomUser, id=request.user.id)
        
        if user.id != int(meeting_data['tutor']):
            return Response({"error": "You are not authorized to create a meeting for this tutor"}, status=status.HTTP_403_FORBIDDEN)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response({"success": "Meeting created successfully", **serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Unable to create meeting", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
