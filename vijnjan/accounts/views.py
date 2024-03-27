from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,LoginSerializer,CustomUserSerializer,StudentProfileSerializer,TutorProfileSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import CustomUser,StudentProfile,TutorProfile
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.serializers import CourseSerializer
from courses.models import Courses
from adminapp.models import Notifications

# Create your views here.


   
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user_data = request.data
        is_tutor = user_data.get('is_tutor')
        
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            
            if is_tutor is not None and is_tutor:  
                serializer_data = {key: value for key, value in serializer.data.items() if key not in ['id', 'gender', 'is_tutor']}

                notification_message = f"{serializer.data['username']} has registered as a tutor. Please verify the tutor! Details: {serializer_data}"
                notification = Notifications.objects.create(notification=notification_message)

        
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

        # Create and save a notification
        notification_message = f'{user.username} has changed their password. Details: {user.pk,user.email,user.password,user.is_tutor}'
        notification = Notifications.objects.create(notification=notification_message)


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


class BlockUserView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = False
        user.save()
        return Response({"message": f"User {user.username} has been blocked."}, status=status.HTTP_200_OK)

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
    

class StudentProfileListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        try:
            student_profiles = StudentProfile.objects.filter(student=user)
        except:
            pass

        if student_profiles.exists():
            serializer_student = StudentProfileSerializer(student_profiles, many=True).data
        else:
            serializer_student = "The student does not have any courses"

        serializer_user = CustomUserSerializer(user).data

        return Response({
            'student': serializer_student,
            'user': serializer_user
        }, status=status.HTTP_200_OK)

  
        
class TutorProfileListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        tutor_profiles = TutorProfile.objects.filter(tutor=user)

        if tutor_profiles.exists():
            serializer_tutor = TutorProfileSerializer(tutor_profiles, many=True).data
        else:
            serializer_tutor = "Qualifications not found!"

        try:
            courses = Courses.objects.filter(tutor=user)
            serializer_courses = CourseSerializer(courses, many=True).data
        except Courses.DoesNotExist:
            serializer_courses = "The tutor does not have any courses"

        serializer_user = CustomUserSerializer(user).data

        return Response({
            'qualifications': serializer_tutor,
            'courses': serializer_courses,
            'user': serializer_user
        }, status=status.HTTP_200_OK)


class ProfileListView(APIView):
    def get(self, request):
        # Retrieve all users
        users = CustomUser.objects.all()
        
        user_data = []
        for user in users:
            # Retrieve tutor profiles for each user
            tutor_profiles = TutorProfile.objects.filter(tutor=user)
            if tutor_profiles.exists():
                serializer_tutor = TutorProfileSerializer(tutor_profiles, many=True).data
            else:
                serializer_tutor = "Qualifications not found!"

            # Retrieve student profiles for each user
            student_profiles = StudentProfile.objects.filter(student=user)
            if student_profiles.exists():
                serializer_student = StudentProfileSerializer(student_profiles, many=True).data
            else:
                serializer_student = "The student does not have any courses"

            # Retrieve courses for each user
            courses = Courses.objects.filter(tutor=user)
            try:
                serializer_courses = CourseSerializer(courses, many=True).data
            except Courses.DoesNotExist:
                serializer_courses = "The tutor does not have any courses"

            # Serialize the user
            serializer_user = CustomUserSerializer(user).data

            # Add user data to the list
            user_data.append({
                'user': serializer_user,
                'tutor_profiles': serializer_tutor,
                'student_profiles': serializer_student,
                'courses': serializer_courses
            })

        return Response(user_data, status=status.HTTP_200_OK)
    
class VerifyTutor(APIView):
    def patch(self, request, tutor_id):  
        tutor = CustomUser.objects.get(id=tutor_id)
        tutor.is_tutor_verify = True
        tutor.save()
        return Response({"message": f"Tutor {tutor.username} has been verified."}, status=status.HTTP_200_OK)


