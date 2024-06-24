from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("about", views.about, name="about"),
    path("start_quiz", views.start_quiz, name="start_quiz"),
    path("quiz", views.quiz, name="quiz"),
    path("results", views.results, name="results"),
]