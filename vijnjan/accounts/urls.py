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
]