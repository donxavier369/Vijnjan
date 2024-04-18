from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
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
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenRefreshView


# Create your views here.


   
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user_data = request.data
        person = user_data.get('person')
        
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            
            if person is not None and person == 'tutor':  
                serializer_data = {key: value for key, value in serializer.data.items() if key not in ['id', 'gender', 'is_tutor']}

                notification_message = f"{serializer.data['username']} has registered as a tutor. Please verify the tutor! Details: {serializer_data}"
                notification = Notifications.objects.create(notification=notification_message)

            print(serializer.errors)
            return Response({"success":True,"message":"User registered succussfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success":False,"message":"Bad request","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        email = request.data.get('email', None)
        message = ""
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if user.person == 'tutor':
                    message = "Logged-in user is a tutor"
                elif user.person == 'student':
                    message="Logged-in user is a student"
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']

                refresh = RefreshToken.for_user(user)
                user_data = CustomUserSerializer(user).data
                return Response({
                    'success': True,
                    'message':message,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'data' : user_data
                }) 
   
            except CustomUser.DoesNotExist:
                return Response({'success':False,"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'success':False,"message": "email field is required"}, status=status.HTTP_400_BAD_REQUEST)
    


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



class ForgotPassword(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"success":False,"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        temporary_password = generate_random_password()
        
        user.set_password(temporary_password)
        user.save()

        # Create and save a notification
        notification_message = f'{user.username} has changed their password. Details: {user.pk,user.email,user.password,user.person}'
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
        return Response({"success":True,"message": "Password Sent Successfully!"}, status=status.HTTP_200_OK)


class BlockUserView(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            return Response({"success":False,"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response({"success":True,"message": f"User {user.username} has been blocked."}, status=status.HTTP_200_OK)   


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, user_id, *args, **kwargs):
        print(request.headers)
        user = CustomUser.objects.get(pk=user_id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"User profile updated successfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Failed to create category due to validation errors.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class AddCertificate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = TutorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"Certificate added successfully","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"success":False,"message":"Failed to add certificate due to validation errors","errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class StudentProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        try:
            student_profiles = StudentProfile.objects.filter(student=user)
        except:
            return Response({"success":False,'message': 'Student not found.'}, status=status.HTTP_400_BAD_REQUEST)


        if student_profiles.exists():
            serializer_student = StudentProfileSerializer(student_profiles, many=True).data
        else:
            serializer_student = "The student does not have any courses"

        serializer_user = CustomUserSerializer(user).data

        return Response({
            'success':True,
            'message':"Successfully fetched student details",
            'student': serializer_student,
            'user': serializer_user
        }, status=status.HTTP_200_OK)

  
        
class TutorProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        try:
            tutor_profiles = TutorProfile.objects.filter(tutor=user)
        except:
            return Response({'success':False,'message': 'Tutor not found.'}, status=status.HTTP_400_BAD_REQUEST)


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
            'success':True,
            'message':'Successfully fetched tutor details',
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
            print(user.id)
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
                'success':True,
                'message':'Data of all user and tutor fetched successfully',
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
        return Response({'success':True,"message": f"Tutor {tutor.username} has been verified."}, status=status.HTTP_200_OK)


class UserProfileEditView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.id)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"User profile edited successfully","data":serializer.data},status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return Response({'success':False,'message': 'Both old_password and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'success':False,'message': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform password validation
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({'success':False,'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'success':True,'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class AddUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        profile_image = data.get('profile_image')

        try:
            queryset = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        if queryset and profile_image:
            custom_user = queryset
            custom_user.profile_image = profile_image
            custom_user.save()
            return Response({'success':True,'message':'Profile image added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'message': 'Either user profile not found or profile image not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        user = request.user

        try:
            queryset = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if queryset:
            queryset.profile_image.delete()
            return Response({'success':True, 'message':'Profile image deleted successfully.'},status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'message': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)





class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            OutstandingToken.objects.filter(token=refresh_token).delete()  # Invalidate refresh token
            return Response({'success':True,"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':False,"message": "Invalid or missing token.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TokenRefreshAPIView(TokenRefreshView):
    pass