from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carousel, Notifications
from .serializers import CarouselSerializer,ListNotificationSerializer,AdminSerializer
from django.shortcuts import get_object_or_404
from courses.models import Courses, Categories
from courses.serializers import CourseSerializer,CategorySerializer
from accounts.models import CustomUser
from rest_framework import generics,status
from accounts.serializers import UserLoginSerializer,CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth.hashers import check_password



class AdminLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if not check_password(password, user.password):
                    return Response({'success': False, "message": "The password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
                if not user.is_superuser:
                    return Response({'success':False,'message':'The user is not an admin'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    user = serializer.validated_data['user']

                    refresh = RefreshToken.for_user(user)
                    user_data = AdminSerializer(user).data
                    return Response({
                        'success': True,
                        'message':'Admin login successfully',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'data' : user_data
                    }) 
    
            except CustomUser.DoesNotExist:
                return Response({'success':False,"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'success':False,"message": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST)
    


class CarouselUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CarouselSerializer(data=request.data)
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():    
                serializer.save()
                return Response({"success":True,"message":"carousel successfully added","data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success":False,"message":"unable to add carousel","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CarouselDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                carousel = Carousel.objects.get(id=id)
                carousel.delete()
                return Response({"success":True,"message":"carousel deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            except Carousel.DoesNotExist:
                return Response({"success":False,"message":"carousel not found"}, status=status.HTTP_404_NOT_FOUND)


class CarouselListView(APIView):
    def get(self, request):
        try:
            carousels = Carousel.objects.all()
            serializer = CarouselSerializer(carousels, many=True)
            return Response({"success":True,"message":"carousel listed successfully","data":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"success":False,"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class TrendingCourseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                course = Courses.objects.get(pk=course_id)
            except Courses.DoesNotExist:
                return Response({"success":False,"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
           
            if course:
                if course.is_trending:
                    course.is_trending = False
                    course.save()
                else:
                    course.is_trending = True
                    course.save()

            # Serialize the updated course data
            serializer = CourseSerializer(course)
            return Response({"success":True,"message":"Course updated successfully","data":serializer.data}, status=status.HTTP_200_OK)
    

class ListNotification(APIView):
    
    def get(self, request):
        try:
            notifications = Notifications.objects.all().order_by('-id')  
            serializer = ListNotificationSerializer(notifications, many=True) 
            return Response({"success":True,"message":"Notification listed successfully","data":serializer.data}, status=status.HTTP_200_OK)  
        except:
            return Response({"success":False,"message":"internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class CreateCourseCategory(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Check if the category already exists
                queryset = Categories.objects.filter(category_name=request.data['category_name'])
                if queryset.exists():
                    return Response({"success":False,"message": f"{request.data['category_name']} category already exists"})
                else:
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"success":True,"message":"Category created successfully","data": serializer.data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"success":False,"message":"failed to create category","error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                # Handle the case when 'category_name' is not found in request data
                return Response({"success":False,"message": "Category name not provided"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle any other unexpected exceptions
                return Response({"success":False,"message":"Internal server error","error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class ListCourseCategory(APIView):
    def get(self, request):
        try:
            categories = Categories.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({"success":True,"message":"Courses listed successfully","data":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"success":False,"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteCourseCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id):
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                category = Categories.objects.get(pk=category_id)
                category.delete()
                return Response({"success":True,"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
            except Categories.DoesNotExist:
                return Response({"success":False,"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success":False,"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
            
class VerifyTutor(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request, tutor_id):
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                tutor = CustomUser.objects.get(id=tutor_id)
            except CustomUser.DoesNotExist:
                return Response({"success":False,"message":"Tutor not found"}, status=status.HTTP_404_NOT_FOUND)
            if tutor.person != 'tutor':
                return Response({"success":False,"message":"This user is not a tutor"}, status=status.HTTP_400_BAD_REQUEST)
            elif tutor.is_tutor_verify :
                return Response({"success":False,"message":"This tutor is already verified"}, status=status.HTTP_200_OK)
            else:
                try:
                    tutor.is_tutor_verify = True
                    tutor.save()
                    return Response({"success":True,"message":"Tutor verified successfully"}, status=status.HTTP_200_OK)
                except:
                    return Response({"success":False,"message":"Unable to verify the tutor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            return Response({"success":False,"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success':False,'message':'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.is_superuser:
            return Response({"success":False,"message": "Given user is not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active = False
            user.save()
            return Response({"success":True,"message": f"User {user.username} has been blocked."}, status=status.HTTP_200_OK)   
        

class UnBlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            admin = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'success': False, 'message': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not admin.is_superuser:
            return Response({"success": False, "message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            user.is_active = True
            user.save()
            return Response({"success": True, "message": f"User {user.username} has been unblocked."}, status=status.HTTP_200_OK)
  