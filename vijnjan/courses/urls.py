from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('createcourse/',views.CourseCreateAPIView.as_view(), name="createcourse"),
    # path('updatecourse/<int:pk>/', views.CoursesUpdateAPIView.as_view(), name="updatecourse"),
    path('deletecourse/<int:pk>/', CourseDeleteAPIView.as_view(), name='deletecourse'),
    path('listcourses/', views.CourseListAPIView.as_view(), name="listcourses"),
    path('listmodules/<int:id>/', views.ModuleListAPIView.as_view(), name="listmodules"),
]


