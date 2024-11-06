"""The view handles the requests and handling data to the webpage."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import generic
from sqlparse.utils import offset

from webpage.models import Recipe, Diet, RecipeStep, Favourite
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from webpage.forms import CustomRegisterForm
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
import random


def register_view(request):
    """
    Register View for user creation.

    :param request: Request from the server.
    """
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')

            # Validate password length
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long")
                return render(request, 'registration/signup.html', {'form': form})

            # Validate password match
            if password != password_confirm:
                messages.error(request, "Passwords do not match")
                return render(request, 'registration/signup.html', {'form': form})

            # Create and log in the user if form is valid
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('recipe_list')
        else:
            # Display validation errors from the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """
    Login view for user login.

    :param request: Request from the server.
    """
    if request.user.is_authenticated:
        return redirect('recipe_list')  # Redirect if already logged in

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('recipe_list')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'registration/login.html', {'messages': messages.get_messages(request)})


def signout_view(request):
    """
    Logout view for user to log user out and redirect to correct URL.

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
        query = self.request.GET.get('query', '')
        difficulty = self.request.GET.get('difficulty')
        filtered_queryset = Recipe.objects.all()
        selected_diet = self.request.GET.get('diet')
        ingredient = self.request.GET.get('ingredient')
        estimated_time = self.request.GET.get('estimated_time', 9999)
        equipment = self.request.GET.get('equipment')
        filter_params = FilterParam(
            offset=400,
            number=view_count,
            includeIngredients=[ingredient.name] if ingredient else [],
            equipment=[equipment.name] if equipment else [],
            diet=[selected_diet.name] if selected_diet else [],
            maxReadyTime=int(estimated_time) if estimated_time else 9999,
            titleMatch=query
        )
        recipe_filter = GetDataProxy(GetDataSpoonacular())
        filtered_recipes = recipe_filter.filter_recipe(filter_params)
        recipe_list = [facade.get_recipe() for facade in filtered_recipes]

        return recipe_list[:view_count]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to increment view_count.

        :param request: HttpRequest from the server.
        """
        if 'increment' in request.POST:
            increment = int(request.POST.get('increment', 0))
            request.session['view_count'] = request.session.get('view_count', 0) + increment
            request.session['button_clicked'] = True
        return redirect(request.path)

    def get_context_data(self, **kwargs):
        """Add the current view_count and diet filter to the context."""
        context = super().get_context_data(**kwargs)
        context['total_recipes'] = Recipe.objects.count()
        context['view_count'] = self.request.session.get('view_count', 0)
        context['diets'] = Diet.objects.all()
        context['selected_diet'] = self.request.GET.get('diet')
        context['estimated_time'] = self.request.GET.get('estimated_time', '')
        context['selected_ingredient'] = self.request.GET.get('ingredient', '')
        context['selected_equipment'] = self.request.GET.get('equipment', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['query'] = self.request.GET.get('query', '')
        context['button_clicked'] = self.request.session.pop('button_clicked',
                                                             False)
        if self.request.user.is_authenticated:
            context['user_favourites'] = Favourite.objects.filter(
                user=self.request.user).values_list('recipe_id', flat=True)
        else:
            context['user_favourites'] = []

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


def random_recipe_view(request):
    """
    Redirects the user to a random recipe detail page.

    :param request: Request from the server.
    """
    recipe_count = Recipe.objects.count()
    if recipe_count > 0:
        random_index = random.randint(0, recipe_count - 1)
        random_recipe = Recipe.objects.all()[random_index]
        return redirect('recipe', pk=random_recipe.id)
    else:
        messages.error(request, "No recipes available.")
        return redirect('recipe_list')


@login_required
def toggle_favourite(request, recipe_id):
    """
    Toggle favourite of a recipe.

    :param request: Request from the server.
    :param recipe_id: Recipe ID.
    """
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        user = request.user
        favourite, created = Favourite.objects.get_or_create(recipe=recipe, user=user)
        if created:
            return JsonResponse({'favourited': True})
        else:
            favourite.delete()
            return JsonResponse({'favourited': False})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)


class UserPageView(generic.ListView):
    """UserPageView view."""

    model = Favourite
    template_name = "user_page.html"
    context_object_name = "favourites"  # Name for use in the template

    def get_queryset(self):
        """Return user favourite recipe."""
        return Favourite.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Extend the context data to include the IDs of the user's favourite recipes."""
        context = super().get_context_data(**kwargs)
        favourite_ids = [f.recipe.id for f in context["favourites"]]
        context["favourite_ids"] = favourite_ids
        return context
