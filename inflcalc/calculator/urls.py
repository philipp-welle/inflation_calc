from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('update_length/', views.update_length, name='update_length'),
]