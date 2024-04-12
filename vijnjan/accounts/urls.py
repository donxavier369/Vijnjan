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
    path('person-login/', PersonLoginView.as_view(), name='person-login'),
    path('tutor-login/', TutorLoginView.as_view(), name='tutor-login'),
    path('edit-profile/<int:pk>/', UserProfileEditView.as_view(), name='edit-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgotpassword/<int:user_id>/', views.ForgotPassword.as_view(), name="forgotpassword"),
    path('add_certificate/', AddCertificate.as_view(), name='add_certificate'),
    path('student-profile/<int:user_id>/', StudentProfileView.as_view(), name='student-profile'),
    path('tutor-profile/<int:user_id>/', TutorProfileView.as_view(), name='tutor-profile'),
    path('usersprofilelist/', views.ProfileListView.as_view(),name='ProfileListView'),
    path('block_user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('verify_tutor/<int:tutor_id>/', VerifyTutor.as_view(), name='verify_tutor'),
    path('add-profile-image/', AddUserProfile.as_view(), name='add_profile_image'),
    path('remove-profile-image/',  DeleteUserProfile.as_view(), name='remove-profile-image'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),

]