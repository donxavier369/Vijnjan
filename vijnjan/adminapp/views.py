from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carouse
from .serializers import CarouselSerializer

class CarouselUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CarouselSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
