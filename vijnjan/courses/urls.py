from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('createcourse/',views.CoursesCreateAPIView.as_view(), name="createcourse"),
    path('updatecourse/<int:pk>/', views.CoursesUpdateAPIView.as_view(), name="updatecourse"),
    path('deletecourse/<int:pk>/', views.CoursesDeleteAPIView.as_view(), name="deletecourse"),
]
