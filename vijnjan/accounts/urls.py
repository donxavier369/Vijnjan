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
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('forgotpassword/<int:user_id>/', views.ForgotPassword.as_view(), name="forgotpassword"),
    path('add_certificate/', AddCertificate.as_view(), name='add_certificate'),
    path('user_profile_update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('student-profile/<int:user_id>/', StudentProfileListView.as_view(), name='student-profile'),
    path('tutor-profile/<int:user_id>/', TutorProfileListView.as_view(), name='tutor-profile'),



]