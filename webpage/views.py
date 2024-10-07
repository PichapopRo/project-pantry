from django.http import HttpResponse
from django.shortcuts import render


def recipes(request):
    return HttpResponse("Hello, world. You're at the polls index.")
