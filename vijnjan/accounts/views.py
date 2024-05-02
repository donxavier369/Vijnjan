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
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from vijnjan.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.exceptions import InvalidToken



# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        date_of_birth = request.data.get('date_of_birth')
        gender = request.data.get('gender')
        person = request.data.get('person')
        password = request.data.get('password')
        if not email:
            return Response({"success": False, "message":"email field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({"success": False, "message":"username field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not date_of_birth:
            return Response({"success": False, "message":"date_of_birth field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not person:
            return Response({"success": False, "message":"person field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"success": False, "message":"password field is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({"success": False, "message": "Invalid email format. Please provide a valid email address (e.g., example@example.com)"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"success": False, "message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username contains special characters
        if any(char in username for char in r'~!@#$%^&*()+=\|{}[]:;"\'<>?,./'):
            return Response({"success": False, "message": "Username cannot contain special characters other than spaces."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if person is valid
        if person not in dict(USER_TYPE_CHOICES).keys():
            return Response({"success": False, "message": "Invalid choice for person. Valid choices are: student, tutor"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if gender is valid
        if gender not in dict(GENDER_CHOICES).keys():
            return Response({"success": False, "message": "Invalid choice for gender. Valid choices are: male, female"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        user = CustomUser.objects.create(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            gender=gender,
            password=hashed_password,
            person=person
        )
        if person is not None and person == 'tutor':  
                notification_message = f"{username} has registered as a tutor. Please verify the tutor! Details: {email,date_of_birth,gender,person}"
                notification = Notifications.objects.create(notification=notification_message)
        return Response({"success": True, "message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        
        

class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        serializer_courses = []
        data = []
        courses = []
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active == False:
                    return Response({'success':False,"message": "User is blocked by admin"}, status=status.HTTP_403_FORBIDDEN)
                if not check_password(password, user.password):
                    return Response({'success': False, "message": "The password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']

                refresh = RefreshToken.for_user(user)
                user_data = CustomUserSerializer(user).data
                refresh = RefreshToken.for_user(user)

                if user.person == 'tutor':
                    tutor_profiles = TutorProfile.objects.filter(tutor=user)
                    if tutor_profiles.exists():
                        serializer_tutor = TutorProfileSerializer(tutor_profiles, many=True).data
                    else:
                        serializer_tutor = []
                    try:
                        tutor_courses = Courses.objects.filter(tutor = user.id)
                    except:
                        tutor_courses = None
                    if tutor_courses:
                        try:
                            serializer_courses = CourseSerializer(tutor_courses, many=True).data
                        except Courses.DoesNotExist:
                            serializer_courses = []
                    
                    data.append({
                        **user_data,
                        'Qualifications': serializer_tutor,
                        'courses': serializer_courses,
                    })
                    return Response({
                        'success': True,
                        'message':"Tutor login successfully",
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'data' : data
                    }) 
                elif user.person == 'student':
                    student_profiles = StudentProfile.objects.filter(student=user)
                    if student_profiles.exists():
                        serializer_student = StudentProfileSerializer(student_profiles, many=True).data
                        for student in serializer_student:
                            courses_ids = student.get('courses')
                            if courses_ids:
                                print("Course IDs:", courses_ids)
                                courses = Courses.objects.filter(id=courses_ids)
                                try:
                                    serializer_courses = CourseSerializer(courses, many=True).data
                                except Courses.DoesNotExist:
                                    serializer_courses = []
                    data.append({
                        **user_data,
                        'courses': serializer_courses
                    })
                    return Response({
                        'success': True,
                        'message':'Student login successfully',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'data' : data
                    }) 
              
   
            except CustomUser.DoesNotExist:
                return Response({'success':False,"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except serializers.ValidationError as error:
                return serializer.login_response()
        else:
            return Response({'success':False,"message": "email and password is required"}, status=status.HTTP_400_BAD_REQUEST)
    


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            return Response({"success":False, "message":"email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
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
            return Response({'success': False, 'message': 'Tutor not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if tutor_profiles.exists():
            serializer_tutor = TutorProfileSerializer(tutor_profiles, many=True).data
        else:
            serializer_tutor = "Qualifications not found!"

        try:
            courses = Courses.objects.filter(tutor=user)
            serializer_courses = CourseSerializer(courses, many=True).data
        except Courses.DoesNotExist:
            serializer_courses = []

        serializer_user = CustomUserSerializer(user).data

        return Response({
            'success': True,
            'message': 'Successfully fetched tutor details',
            'qualifications': serializer_tutor,
            'courses': serializer_courses,
            'user': serializer_user
        }, status=status.HTTP_200_OK)




class ProfileListView(APIView):
    def get(self, request):
        # Retrieve all users
        users = CustomUser.objects.all()
        is_tutor = ""
        
        serializer_courses = []
        tutor_data = []
        student_data = []
        for user in users:
            # Retrieve tutor profiles for each user
            is_tutor = user.person
            tutor_profiles = TutorProfile.objects.filter(tutor=user)
            if tutor_profiles.exists():
                serializer_tutor = TutorProfileSerializer(tutor_profiles, many=True).data
            else:
                serializer_tutor = []

            # Retrieve student profiles for each user
            student_profiles = StudentProfile.objects.filter(student=user)
            if student_profiles.exists():
                serializer_student = StudentProfileSerializer(student_profiles, many=True).data
                for student in serializer_student:
                    courses_ids = student.get('courses')
                    if courses_ids:
                        print("Course IDs:", courses_ids)
                        courses = Courses.objects.filter(id=courses_ids)
                        try:
                            serializer_courses = CourseSerializer(courses, many=True).data
                        except Courses.DoesNotExist:
                            serializer_courses = []

            else:
                serializer_student = []
            
            # Retrieve courses for each user
            
            # Serialize the user
            serializer_user = CustomUserSerializer(user).data
            if user.person == 'tutor':
                tutor_data.append({
                    **serializer_user,
                    'Qualifications': serializer_tutor,
                })

            elif user.person == 'student':
                student_data.append({
                    **serializer_user,
                    'courses': serializer_courses
                })
        return Response({"success": True, "message": "Data of all user and tutor fetched successfully", "tutor_profile": tutor_data, "student_profile":student_data}, status=status.HTTP_200_OK)




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
            if not queryset:
                return Response({'success':False,'message': 'User profile not found '}, status=status.HTTP_400_BAD_REQUEST)
            elif not profile_image:
                return Response({'success':False,'message': 'Profile image not provided.'}, status=status.HTTP_400_BAD_REQUEST)

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
    def handle_exception(self, exc):
        if isinstance(exc, InvalidToken):
            return Response({'success': False, 'message': 'Refresh token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
