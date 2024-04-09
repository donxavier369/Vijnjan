from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('createcourse/',views.CourseCreateAPIView.as_view(), name="createcourse"),
    # path('updatecourse/<int:pk>/', views.CoursesUpdateAPIView.as_view(), name="updatecourse"),
    path('deletecourse/<int:pk>/', CourseDeleteAPIView.as_view(), name='deletecourse'),
    path('listcourses/', views.CourseListAPIView.as_view(), name="listcourses"),
    path('listmodules/<int:course_id>/<int:user_id>/', views.ModuleListAPIView.as_view(), name="listmodules"),
    path('list_trending_courses/', views.TrendingCourseListAPIView.as_view(), name="lis_trending_tcourses"),
    path('category_courses/', CategoryCourseListView.as_view(), name='category_courses'),

]


