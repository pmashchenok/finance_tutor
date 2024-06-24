from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("about", views.about, name="about"),
    path("quiz", views.quiz, name="quiz"),
]