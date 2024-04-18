from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import *


from rest_framework_simplejwt.views import(
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('edit-profile/<int:pk>/', UserProfileEditView.as_view(), name='edit_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/<int:user_id>/', views.ForgotPassword.as_view(), name="forgot_password"),
    path('add-certificate/', AddCertificate.as_view(), name='add_certificate'),
    path('student-profile/<int:user_id>/', StudentProfileView.as_view(), name='student-profile'),
    path('tutor-profile/<int:user_id>/', TutorProfileView.as_view(), name='tutor_profile'),
    path('users-profile-list/', views.ProfileListView.as_view(),name='users_profile_list'),
    path('block-user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('verify-tutor/<int:tutor_id>/', VerifyTutor.as_view(), name='verify_tutor'),
    path('add-profile-image/', AddUserProfile.as_view(), name='add_profile_image'),
    path('remove-profile-image/',  DeleteUserProfile.as_view(), name='remove-profile-image'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    
]