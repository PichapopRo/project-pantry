from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


# View to display a single recipe's details
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe,
                               pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('recipe')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
