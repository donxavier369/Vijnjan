from django.urls import path
from .views import *

urlpatterns = [
    path('admin-login/', AdminLoginView.as_view(),name='admin_login'),
    path('carousel-upload/', CarouselUploadView.as_view(), name='carousel_upload'),
    path('delete-carousel/<int:id>/', CarouselDeleteView.as_view(), name="delete_carousel"),
    path('list-carousel/', CarouselListView.as_view(), name="list_carousel"),
    path('update-trending/<int:course_id>/', TrendingCourseUpdateView.as_view(), name='update_trending'),
    path('notifications/', ListNotification.as_view(), name='list_notifications'),
    path('create-category/', CreateCourseCategory.as_view(), name='create_category'),
    path('list-categories/', ListCourseCategory.as_view(), name='list_categories'),
    path('delete-category/<int:category_id>/', DeleteCourseCategory.as_view(), name='delete_category'),
    path('verify-tutor/<int:tutor_id>/', VerifyTutor.as_view(), name='verify_tutor')

]
    