from django.views import generic
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from webpage.forms import CustomRegisterForm
from webpage.modules.proxy import RecipeFilter


def register_view(request):
    """
    Register VIew for user creation.

    :param request: Request from the server.
    """
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
            return redirect('recipe_list')  # Redirect to home or another page
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """
    Login view for user login.

    :param request: Request from the server.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipe_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/login.html')


def signout_view(request):
    """
    Logout view for user to log user out and redirect to correct URL

    :param request: Request from the server.
    """
    logout(request)
    return redirect("recipe_list")


class RecipeListView(generic.ListView):
    """RecipeList view."""

    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        """Return recipes filtered by diet, ingredient, max cooking time, and limited by view_count."""
        view_count = self.request.session.get('view_count', 0)
        recipe_filter = RecipeFilter()

        # Retrieve parameters from the request
        selected_diet = self.request.GET.get('diet')
        ingredient = self.request.GET.get('ingredient')
        max_cooking_time = self.request.GET.get('max_cooking_time')

        # Start with all recipes
        filtered_queryset = Recipe.objects.all()

        # Apply diet filter if selected
        if selected_diet:
            filtered_queryset = recipe_filter.filter_by_diet(selected_diet)

        # Apply ingredient filter if specified
        if ingredient:
            filtered_queryset = filtered_queryset.intersection(
                recipe_filter.filter_by_ingredient(ingredient))

        # Apply max cooking time filter if specified
        if max_cooking_time:
            try:
                max_cooking_time = int(max_cooking_time)  # Convert to int
                filtered_queryset = filtered_queryset.intersection(
                    recipe_filter.filter_by_max_cooking_time(max_cooking_time))
            except ValueError:
                pass  # Handle the case where max_cooking_time is not a valid integer

        return filtered_queryset[:view_count]  # Limit results based on view_count

    def post(self, request, *args, **kwargs):
        """Handle POST request to increment view_count."""
        if 'increment' in request.POST:
            increment = int(request.POST.get('increment', 0))
            request.session['view_count'] = request.session.get('view_count', 0) + increment
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the current view_count and diet filter to the context."""
        context = super().get_context_data(**kwargs)
        context['total_recipes'] = Recipe.objects.count()
        context['view_count'] = self.request.session.get('view_count', 0)
        context['diets'] = Diet.objects.all()
        context['selected_diet'] = self.request.GET.get('diet')

        return context


class RecipeView(generic.DetailView):
    """RecipeView view."""
    template_name = 'recipes/description.html'
    model = Recipe
    context_object_name = 'recipe'


class StepView(generic.DetailView):
    """StepView view for displaying the steps of a recipe."""
    template_name = 'recipes/steps.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        """Add steps directly from RecipeStep model to the context."""
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['steps'] = RecipeStep.objects.filter(recipe=recipe).order_by('number')
        return context
