from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    x = 10
    y = 30
    return render(request, 'index.html', {'name': 'Jarvis'})
