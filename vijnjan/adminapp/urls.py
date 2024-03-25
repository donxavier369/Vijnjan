from django.urls import path
from .views import CarouselUploadView, CarouselDeleteView, CarouselListView, TrendingCourseUpdateView

urlpatterns = [
    path('carousel_upload/', CarouselUploadView.as_view(), name='carousel-upload'),
    path('delete_carousel/<int:id>/', CarouselDeleteView.as_view(), name="delete_carousel"),
    path('list_carousel/', CarouselListView.as_view(), name="list_carousel"),
    path('update_trending/<int:course_id>/', TrendingCourseUpdateView.as_view(), name='update-trending'),

]
