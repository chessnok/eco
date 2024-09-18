from django.urls import path

from events.views import register_organizer

urlpatterns = [
    path('register_organizer/', register_organizer, name='register_organizer'),
]