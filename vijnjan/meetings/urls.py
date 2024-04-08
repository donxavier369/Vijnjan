from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('createmeeting/',MeetingApiView.as_view(), name="createmeeting"),
]