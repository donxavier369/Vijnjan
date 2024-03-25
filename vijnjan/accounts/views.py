from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,LoginSerializer,TutorProfileSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import CustomUser
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from rest_framework.permissions import IsAuthenticated



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


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



class ForgotPassword(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        temporary_password = generate_random_password()
        
        user.set_password(temporary_password)
        user.save()

        email = user.email
        subject = 'Your Vijnajn Login Password'
        message = f'Dear {user.username},\n\n' \
                  f'We noticed that you are having trouble accessing your Vijnajn account. No worries! To assist you in regaining access, we have generated a new password for you.\n\n' \
                  f'Your new login credentials are as follows:\n\n' \
                  f'Username: {email}\n' \
                  f'password: {temporary_password}\n\n' \
                  f'Please use this temporary password to access your Vijnajn account and reset your password immediately after login.\n\n' \
                  f'Best regards,\nTeam Vijnjan'
        from_email = settings.EMAIL_HOST_USER  

        send_mail(subject, message, from_email, [email])
        return Response({"message": "Password Sent Successfully!"}, status=status.HTTP_200_OK)
    


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddCertificate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TutorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)