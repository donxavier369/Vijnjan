from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Meatings
from .serializers import MeatingSerializer
from rest_framework import status

# Create your views here.

class MeetingApiView(APIView):
    serializer_class = MeatingSerializer 

    def post(self,request):
        meeting_data = request.data
        print(request.data,"data")
        serializer = self.serializer_class(data=meeting_data)
        if serializer.is_valid():
            meeting_name = meeting_data.get('meating_name', '')
            print(meeting_name,"ooooooooooo")
            meeting_link = f"https://fanzkart.shop/{meeting_name.replace(' ','_')}"
            serializer.save(link=meeting_link)
            return Response({**serializer.data, 'link':meeting_link}, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        




