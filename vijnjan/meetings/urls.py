from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('generate-meeting-link/', GenerateMeetingLink.as_view(), name="generate-meeting-link"),
    path('createmeeting/',MeetingApiView.as_view(), name="createmeeting"),
]