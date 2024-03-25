from django.urls import path
from .views import CarouselUploadView

urlpatterns = [
    path('carousel_upload/', CarouselUploadView.as_view(), name='carousel-upload'),
]
