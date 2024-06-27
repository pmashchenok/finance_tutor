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

# testing.make_db() # TODO
test = testing.TestState()
# test.get_question()
test.question_list = [testing.Question(1, "Тестовый вопрос 1"), 
                      testing.Question(2, "Тестовый вопрос 2"),
                      testing.Question(3, "Тестовый вопрос 3"),
                      testing.Question(4, "Тестовый вопрос 4"),
                      testing.Question(5, "Тестовый вопрос 5"),
                      testing.Question(6, "Тестовый вопрос 6"),
                      testing.Question(7, "Тестовый вопрос 7"),
                      testing.Question(8, "Тестовый вопрос 8"),
                      testing.Question(9, "Тестовый вопрос 9"),
                      testing.Question(10, "Тестовый вопрос 10")]
test.answers_list = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]
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
    return render(request, 'profile.html')


def start_quiz(request):
    return render(request, "main_site/start_quiz.html")


def quiz(request):
    test_context = json.dumps([q.__dict__ for q in test.question_list])
    return render(request, "main_site/quiz.html", context={"test": test_context})

def results(request):
    test.score = 0
    if request.method == "GET":
        answers = json.loads(f"[{request.GET['results']}]")
        test.check_answers(answers)
        return render(request, "main_site/results.html", context={"score": test.score})
    
def start_game(request):
    return render(request, "main_site/start_game.html")

def chara_input(request):
    return render(request, "main_site/chara_input.html")

def product_input(request):
    global character
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        citizenship = request.POST["ctzn"]
        income = request.POST["income"]
        work_exp = request.POST["work_exp"]
        client = request.POST["client"] == "y"
        character = gamec.Character(name, age, citizenship, income, work_exp, income, client)
        context = json.dumps(character.__dict__())
        print(context, file=sys.stderr)
        return render(request, "main_site/product_input.html", context={ "character": context })

def game(request):
    if request.method == "POST":
        product_name = request.POST["product_name"]
        product = None
        product_type = None
        match product_name: 
            case "mainloan":
                product_type = products.ProductType.LOAN_MAIN
                is_client = character.client
                duration = request.POST["duration"]
                amnt = request.POST["amnt"]
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO не знаю как это определяется я просто взял
                # мин. значения с сайта
                interest_1st_period = 0.25
                duration_1st_period = 6
                product = products.MainLoan(is_client, duration, amnt, has_furry_zero,
                                            interest_1st_period, duration_1st_period)
            case "targetloan":
                product_type = products.ProductType.LOAN_TARGET
                is_client = character.client
                duration = request.POST["duration"]
                amnt = request.POST["amnt"]
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO 
                year_interest = 0.25
                product = products.TargetLoan(is_client, duration, amnt, has_furry_zero, year_interest)
            case "cc2y":
                product_type = products.ProductType.CC_2Y
                # TODO Как определяется предел?
                product = products.CC2Years(0, 100000, True, 0)
            case "cc200d":
                # TODO
                product_type = products.ProductType.CC_200D
                product = products.CC200Days(0, 100000, True, 0)
        state = gamec.GameState(character, product, product_type)
        context = json.dumps(state.__dict__())
        print(context)
        return render(request, "main_site/game.html", context={"state": context})
