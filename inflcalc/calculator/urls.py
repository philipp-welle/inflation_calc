from django.urls import path

from . import views

urlpatterns = [
    path("calc/", views.calc, name="calc"),
    path("", views.landing, name="landing"),
    path('update_length/', views.update_length, name='update_length'),
]