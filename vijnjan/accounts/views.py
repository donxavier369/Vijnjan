from django.shortcuts import render
from rest_framework import generics,status
from .serializer import RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


   
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

