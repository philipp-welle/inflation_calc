from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("landing/", views.landing, name="landing"),
    path('update_length/', views.update_length, name='update_length'),
]