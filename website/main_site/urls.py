from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("about", views.about, name="about"),
    path("start_quiz", views.start_quiz, name="start_quiz"),
    path("question", views.question, name="question"),
]