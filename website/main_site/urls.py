from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='main'),
    path("about", views.about, name="about"),
    path("start_quiz", views.start_quiz, name="start_quiz"),
    path("quiz", views.quiz, name="quiz"),
    path("results", views.results, name="results"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path("start_game", views.start_game, name="start_game"),
    path("chara_input", views.chara_input, name="chara_input"),
    path("product_input", views.product_input, name="product_input"),
    path("game", views.game, name="game")
]