from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import *


def recipes(request):
    return render(request, 'recipes/recipe.html')


class IndexView(generic.ListView):
    """Index view."""

    template_name = 'recipes/recipe.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        """Return 5 recipes."""
        all_recipes = Recipe.objects.all()
        return all_recipes[:5]
