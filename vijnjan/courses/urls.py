from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('create-course/',views.CourseCreateAPIView.as_view(), name="create_course"),
    path('create-module/', ModuelCreateAPIView.as_view(), name="create_module"),
    path('delete-course/<int:pk>/', CourseDeleteAPIView.as_view(), name='delete_course'),
    path('list-courses/', views.CourseListAPIView.as_view(), name="list_courses"),
    path('list-modules/<int:course_id>/', views.ModuleListAPIView.as_view(), name="list_modules"),
    path('list-trending-courses/', views.TrendingCourseListAPIView.as_view(), name="list_trending_courses"),
    path('category_courses/', CategoryCourseListView.as_view(), name='category_courses'),
    path('add-files/', views.AddVideoPptAPI.as_view(), name="add-files"),
    path('get-files/<int:tutor_id>/', views.GetFiles.as_view(), name='get-files'),
]


