"""Notifications URL Configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("subscribe_info", views.subscribe_info, name="subscribe_info"),
    path("serviceworker", views.serviceworker, name="serviceworker"),
]
