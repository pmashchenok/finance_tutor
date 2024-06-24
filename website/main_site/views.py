from django.shortcuts import render
from django.http import HttpResponse
from . import testing
import json
import sys

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


def index(request):
    return render(request, "main_site/index.html")


def about(request):
    return render(request, "main_site/about.html")


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