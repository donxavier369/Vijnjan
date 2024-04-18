from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('generate-meeting-link/', GenerateMeetingLink.as_view(), name="generate_meeting_link"),
    path('create-meeting/',MeetingApiView.as_view(), name="create_meeting"),
]