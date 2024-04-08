from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Meetings
from .serializers import MeetingSerializer
from rest_framework import status
from courses.models import Courses
from django.utils.crypto import get_random_string


# Create your views here.




class MeetingApiView(APIView):
    serializer_class = MeetingSerializer

    def post(self, request):
        meeting_data = request.data
        serializer = self.serializer_class(data=meeting_data)
        
        if serializer.is_valid():
            # Generate a unique link
            meeting_link = "https://fanzkart.shop/" + get_random_string(length=10)
            
            # Save the meeting with the generated link
            serializer.save(link=meeting_link)
            
            return Response({**serializer.data, 'link': meeting_link}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)