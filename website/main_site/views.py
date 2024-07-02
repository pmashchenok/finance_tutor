from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import testing
import json
import sys
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from . import gamec
from . import products

test = None
character = None
state = None

def index(request):
    return render(request, "main_site/index.html")


def about(request):
    return render(request, "main_site/about.html")


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('profile')
        except IntegrityError:
            error_message = "Пользователь с таким именем уже существует."
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль!'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user, 'score': request.user.profile.score})


def start_quiz(request):
    return render(request, "main_site/start_quiz.html")


def quiz(request):
    global test
    test = testing.TestState()
    test.get_question_list()
    test_context = json.dumps([q.__dict__ for q in test.question_list])
    return render(request, "main_site/quiz.html", context={"test": test_context})


def results(request):
    global test
    test.score = 0
    if request.method == "GET":
        answers = json.loads(f"[{request.GET['results']}]")
        test.check_answers(answers)
        rating = test.rating()
        user = request.user
        if user.is_authenticated:
            user.profile.score += round(rating, 2)
            user.profile.save()
        return render(request, "main_site/results.html", context={"score": test.score, "rating": rating})
    
def start_game(request):
    global state
    state = None
    return render(request, "main_site/start_game.html")

def chara_input(request):
    global state
    state = None
    return render(request, "main_site/chara_input.html")

def product_input(request):
    global state
    state = None
    global character
    if request.method == "POST":
        name = request.POST["name"]
        age = int(request.POST["age"])
        citizenship = request.POST["ctzn"]
        income = int(request.POST["income"])
        work_exp = int(request.POST["work_exp"])
        client = request.POST["client"] == "y"
        rating = 0
        character = gamec.Character(name, age, citizenship, income, work_exp, income, client, rating)
        context = json.dumps(character.__dict__())
        print(context, file=sys.stderr)
        return render(request, "main_site/product_input.html", context={ "character": context })

def game(request):
    global state
    if request.method == "POST":
        if state is None:
            state = gamec.GameState.start(character, request)
            state_context = json.dumps(state.__dict__())
            print(state_context)
        else:
            game_input = int(request.POST["game_input"])
            state.progress(game_input)
            state_context = json.dumps(state.__dict__())
            user = request.user
            if user.is_authenticated:
                user.profile.score += round(state.char.rating, 2)
                user.profile.save()
        return render(request, "main_site/game.html", context={"state": state_context, 
                                                               "annuity": str(state.product.annuity_payment())})
