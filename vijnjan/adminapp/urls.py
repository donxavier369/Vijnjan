from django.urls import path
from .views import *

urlpatterns = [
    path('carousel_upload/', CarouselUploadView.as_view(), name='carousel-upload'),
    path('delete_carousel/<int:id>/', CarouselDeleteView.as_view(), name="delete_carousel"),
    path('list_carousel/', CarouselListView.as_view(), name="list_carousel"),
    path('update_trending/<int:course_id>/', TrendingCourseUpdateView.as_view(), name='update-trending'),
    path('notifications/', ListNotification.as_view(), name='list_notifications'),
    path('create_category/', CreateCourseCategory.as_view(), name='create_category'),
    path('list_categories/', ListCourseCategory.as_view(), name='list_categories'),
    path('delete_category/<int:category_id>/', DeleteCourseCategory.as_view(), name='delete_category'),
    path('verify-tutor/<int:tutor_id>/', VerifyTutor.as_view(), name='verify-tutor')

]
    