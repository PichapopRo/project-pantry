from django.views import generic
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from webpage.forms import CustomRegisterForm


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')

            # Validate password length
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 "
                                        "characters long")
                return render(request, 'registration/signup.html',
                              {'form': form})

            # Validate password match
            if password != password_confirm:
                messages.error(request, "Passwords do not match")
                return render(request, 'registration/signup.html',
                              {'form': form})

            # If everything is fine, create the user
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to home or another page
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


class RecipeListView(generic.ListView):
    """RecipeList view."""

    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        """Return recipes limited by view_count."""
        view_count = self.request.session.get('view_count', 0)
        all_recipes = Recipe.objects.all()
        return all_recipes[:view_count]

    def post(self, request, *args, **kwargs):
        """Handle POST request to increment view_count."""
        if 'increment' in request.POST:
            increment = int(request.POST.get('increment', 0))
            request.session['view_count'] = request.session.get('view_count', 0) + increment
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the current view_count to the context."""
        context = super().get_context_data(**kwargs)
        context['total_recipes'] = Recipe.objects.count()
        context['view_count'] = self.request.session.get('view_count', 0)
        return context


class RecipeView(generic.DetailView):
    """RecipeView view."""
    template_name = 'recipes/description.html'
    model = Recipe
    context_object_name = 'recipe'


class StepView(generic.DetailView):
    """StepView view."""
    template_name = 'recipes/steps.html'
    model = Recipe
    context_object_name = 'recipe'
