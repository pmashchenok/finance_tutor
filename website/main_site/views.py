from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "main_site/index.html")


def about(request):
    return render(request, "main_site/about.html")

