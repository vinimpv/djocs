from django.shortcuts import render
from django.http import HttpResponse


def index(request) -> HttpResponse:
    return render(request, "index.html")
