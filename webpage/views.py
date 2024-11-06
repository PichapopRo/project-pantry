"""The view handles the requests and handling data to the webpage."""
from decimal import Decimal
import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic

from pantry import settings
from webpage.models import Recipe, Diet, RecipeStep, Favourite, Ingredient, Equipment
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from webpage.forms import CustomRegisterForm, RecipeForm
from webpage.modules.builder import NormalRecipeBuilder
from webpage.modules.image_to_url import upload_image_to_imgur
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
import random
import json


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
        recipe_filter = GetDataProxy(GetDataSpoonacular(), filtered_queryset)
        selected_diet = self.request.GET.get('diet')
        ingredient = self.request.GET.get('ingredient')
        estimated_time = self.request.GET.get('estimated_time')
        equipment = self.request.GET.get('equipment')
        if query:
            filtered_queryset = recipe_filter.find_by_name(query)
        if selected_diet:
            filtered_queryset = recipe_filter.filter_by_diet(selected_diet)
        if ingredient:
            filtered_queryset = filtered_queryset.intersection(
                recipe_filter.filter_by_ingredient(ingredient))
        if equipment:
            filtered_queryset = filtered_queryset.intersection(
                recipe_filter.filter_by_equipment(equipment))
        if estimated_time:
            try:
                estimated_time = int(estimated_time)  # Convert to int
                filtered_queryset = filtered_queryset.intersection(
                    recipe_filter.filter_by_max_cooking_time(estimated_time))
            except ValueError:
                pass
        if difficulty:
            filtered_queryset = recipe_filter.filter_by_difficulty(difficulty)
        return filtered_queryset[:view_count]

    def post(self, request, *args, **kwargs):
        """Handle POST request to increment view_count."""
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
            context['user_favorites'] = Favourite.objects.filter(
                user=self.request.user).values_list('recipe_id', flat=True)
        else:
            context['user_favorites'] = []

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
    """Redirects the user to a random recipe detail page."""
    recipe_count = Recipe.objects.count()
    if recipe_count > 0:
        random_index = random.randint(0, recipe_count - 1)
        random_recipe = Recipe.objects.all()[random_index]
        return redirect('recipe', pk=random_recipe.id)
    else:
        messages.error(request, "No recipes available.")
        return redirect('recipe_list')


@login_required
def toggle_favorite(request, recipe_id):
    """
    Toggle favorite of a recipe.

    :param request: Request from the server.
    :param recipe_id: Recipe ID.
    """
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        user = request.user
        favorite, created = Favourite.objects.get_or_create(recipe=recipe, user=user)
        if created:
            return JsonResponse({'favorited': True})
        else:
            favorite.delete()
            return JsonResponse({'favorited': False})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)


class AddRecipeView(generic.CreateView):
    model = Recipe
    fields = ['name', 'description', 'estimated_time', 'image']
    template_name = 'recipes/add_recipe.html'
    success_url = '/recipes/'

    def form_valid(self, form):
        print("Incoming form data:", self.request.POST)
        builder = NormalRecipeBuilder(name=form.cleaned_data['name'], user=self.request.user)
        builder.build_details(
            description=form.cleaned_data['description'],
        )
        builder.build_details(estimated_time=form.cleaned_data['estimated_time'])
        print(form.cleaned_data['description'])
        print(form.cleaned_data['estimated_time'])
        ingredients_data = self.request.POST.get('ingredients_data')
        if ingredients_data:
            ingredients = json.loads(ingredients_data)
            for ingredient_entry in ingredients:
                try:
                    amount, unit, name = self.parse_ingredient_input(ingredient_entry)
                    ingredient, _ = Ingredient.objects.get_or_create(name=name)
                    builder.build_ingredient(ingredient=ingredient, amount=amount, unit=unit)
                except Exception as e:
                    print(f"Error parsing ingredient '{ingredient_entry}': {e}")
        equipments_data = self.request.POST.get('equipments_data')
        if equipments_data:
            equipments = json.loads(equipments_data)
            for equipment_entry in equipments:
                try:
                    amount, name = self.parse_equipment_input(equipment_entry)
                    equipment, _ = Equipment.objects.get_or_create(name=name)
                    builder.build_equipment(equipment=equipment)
                except Exception as e:
                    print(f"Error parsing equipment '{equipment_entry}': {e}")
        steps_data = self.request.POST.get('steps_data')
        if steps_data:
            steps = json.loads(steps_data)
            for step_entry in steps:
                try:
                    builder.build_step(step_entry)
                except Exception as e:
                    print(f"Error adding step '{step_entry}': {e}")
        builder.build_recipe().save()
        return JsonResponse({'message': 'Recipe added successfully!'}, status=201)

    def parse_ingredient_input(self, ingredient_entry):
        """Parse the ingredient input string and return amount, unit, and name."""
        match = re.match(r'(\d+(?:\.\d+)?)\s+([a-zA-Z]+)\s+(.+)', ingredient_entry)
        if match:
            amount = Decimal(match.group(1))
            unit = match.group(2)
            name = match.group(3)
            return amount, unit, name
        else:
            return Decimal(1), "", ingredient_entry

    def parse_equipment_input(self, equipment_entry):
        """Parse the equipment input string and return amount and name."""
        match = re.match(r'(\d+(?:\.\d+)?)\s+(.+)', equipment_entry)
        if match:
            amount = int(match.group(1))
            name = match.group(2)
            return amount, name
        else:
            return 1, equipment_entry  # Default amount 1 if parsing fails
