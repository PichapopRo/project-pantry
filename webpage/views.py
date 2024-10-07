from django.http import HttpResponse
from django.shortcuts import render


def recipes(request):
    return render(request, 'recipes/recipe.html')
