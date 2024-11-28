"""The view handles the requests and handling data to the webpage."""
from decimal import Decimal
import re
from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import generic
from pantry import settings
from webpage.models import Recipe, Diet, RecipeStep, Favourite, Ingredient, Equipment, Nutrition
from webpage.modules.ai_advisor import AIRecipeAdvisor
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from webpage.forms import CustomRegisterForm
from webpage.modules.builder import NormalRecipeBuilder
from webpage.modules.image_to_url import upload_image_to_imgur
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from webpage.utils import login_with_backend
import random
import json
import logging
from webpage.modules.status_code import StatusCode


logger = logging.getLogger("Views")


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
            login_with_backend(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
    message = messages.get_messages(request)
    message.used = True
    if request.user.is_authenticated:
        return redirect('recipe_list')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
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
        ingredient_data = self.request.GET.get('ingredients_data', '[]')
        diets_data = self.request.GET.get('diets_data', '[]')
        estimated_time = self.request.GET.get('estimated_time', None)
        ingredients = json.loads(ingredient_data)
        selected_diets = json.loads(diets_data)
        try:
            estimated_time = int(estimated_time) if estimated_time else 9999
        except ValueError:
            estimated_time = 9999

        logger.debug(f"Query: {query}")
        logger.debug(f"Ingredients: {ingredients}")
        logger.debug(f"Diets: {selected_diets}")
        logger.debug(f"Estimated time: {estimated_time}")
        filter_params = FilterParam(
            offset=1,
            number=view_count,
            includeIngredients=ingredients,
            diet=selected_diets,
            maxReadyTime=estimated_time,
            titleMatch=query
        )

        logger.debug(f"Filter parameters: {filter_params}")
        recipe_filter = GetDataProxy(GetDataSpoonacular())
        filtered_recipes = recipe_filter.filter_recipe(filter_params)

        logger.debug(f"Filtered recipes response: {filtered_recipes}")

        return [facade.get_recipe() for facade in filtered_recipes][:view_count]

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

    def get_context_data(self, **kwargs):
        """Add steps directly from RecipeStep model to the context."""
        context = super().get_context_data(**kwargs)
        recipe: Recipe = self.get_object()
        context['can_favorite'] = None if recipe.status != StatusCode.APPROVE.value[0] else True
        context['steps'] = RecipeStep.objects.filter(recipe=recipe).order_by('number')
        context['equipments'] = Recipe.get_equipments(recipe)
        if self.request.user.is_authenticated:
            context['user_favourites'] = Favourite.objects.filter(
                user=self.request.user).values_list('recipe_id', flat=True)
        else:
            context['user_favourites'] = []
        return context
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Get the Recipe class for the user. If the recipe is not approved, it will redirect to the main page.
        
        :param request: The request from the page.
        :return: A HTTP Response. 
        """
        recipe: Recipe = self.get_object()
        if recipe.status != StatusCode.APPROVE.value[0] and recipe.poster_id.id != request.user.id:
            return redirect('recipe_list')
        return super().get(request, *args, **kwargs)
    

def random_recipe_view(request):
    """
    Redirects the user to a random recipe detail page.

    :param request: Request from the server.
    """
    random_recipes = Recipe.objects.filter(status=StatusCode.APPROVE.value[0])
    if random_recipes.count() > 0:
        random_index = random.randint(0, random_recipes.count() - 1)
        random_recipe = random_recipes[random_index]
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


class AddRecipeView(generic.CreateView):
    """View for adding recipe page."""

    model = Recipe
    fields = ['name', 'description', 'estimated_time', 'image']
    template_name = 'recipes/add_recipe.html'
    success_url = '/recipes/'

    def get_context_data(self, **kwargs):
        """
        Get diet context from the existing diet.

        :return context: Return existing diet model context to use in html.
        """
        context = super().get_context_data(**kwargs)
        context['diets'] = Diet.objects.all()

        return context

    def form_valid(self, form):
        """
        Process the submitted recipe form, including details, image upload, ingredients, diets, equipment, and steps.

        :param form: The RecipeForm instance containing validated data for
        creating a new recipe.
        :return JsonResponse: A JSON response indicating the success
        of the recipe creation.
        """
        builder = NormalRecipeBuilder(name=form.cleaned_data['name'], user=self.request.user)
        self.process_detail(builder, form)
        self.process_image(builder, form)
        self.process_ingredients(builder)
        self.process_diets(builder)
        self.process_equipments(builder)
        self.process_steps(builder)
        self.process_nutrition(builder)
        builder.build_recipe().status = StatusCode.PENDING.value[0]
        builder.build_difficulty()
        self.process_status(builder)
        return JsonResponse({'message': 'Recipe added successfully!'}, status=201)

    def process_detail(self, builder: NormalRecipeBuilder, form):
        """
        Process the detail data of the recipe.

        :param builder: Recipe Builder instance.
        :param form: The RecipeForm instance containing validated data.
        """
        builder.build_details(
            description=form.cleaned_data['description'],
        )
        builder.build_details(estimated_time=form.cleaned_data['estimated_time'])

    def process_image(self, builder: NormalRecipeBuilder, form):
        """
        Process the image data of the recipe.

        :param builder: Recipe Builder instance.
        :param form: The RecipeForm instance containing validated data.
        """
        image = form.files.get('photo')
        if image:
            client_id = settings.IMGUR_CLIENT_ID
            image_url = upload_image_to_imgur(image, client_id)
            if image_url:
                builder.build_details(image=image_url)

    def process_ingredients(self, builder: NormalRecipeBuilder):
        """
        Process the ingredients data page of the recipe.

        :param builder: Recipe Builder instance.
        """
        ingredients_data = self.request.POST.get('ingredients_data')
        if ingredients_data:
            ingredients = json.loads(ingredients_data)
            for ingredient_entry in ingredients:
                try:
                    amount, unit, name = self.parse_ingredient_input(ingredient_entry)
                    ingredient, _ = Ingredient.objects.get_or_create(name=name)
                    builder.build_ingredient(ingredient=ingredient, amount=amount, unit=unit)
                except Exception as e:
                    logger.error(f"Error parsing ingredient '{ingredient_entry}': {e}")

    def process_diets(self, builder: NormalRecipeBuilder):
        """
        Process the diets data of the recipe.

        :param builder: Recipe Builder instance.
        """
        diets_data = self.request.POST.get('diets_data')
        if diets_data:
            try:
                diet_names = json.loads(diets_data)
                for diet_name in diet_names:
                    diet, created = Diet.objects.get_or_create(name=diet_name)
                    builder.build_diet(diet)
            except Exception as e:
                logger.error(f"Error parsing diets '{diets_data}': {e}")

    def process_equipments(self, builder: NormalRecipeBuilder):
        """
        Process the equipments of the recipe.

        :param builder: Recipe Builder instance.
        """
        equipments_data = self.request.POST.get('equipment_data')
        if equipments_data:
            equipments = json.loads(equipments_data)
            for equipment_entry in equipments:
                try:
                    amount, name = self.parse_equipment_input(equipment_entry)
                    equipment, _ = Equipment.objects.get_or_create(name=name)
                    builder.build_equipment(equipment=equipment)
                except Exception as e:
                    logger.error(f"Error parsing equipment '{equipment_entry}': {e}")

    def process_steps(self, builder: NormalRecipeBuilder):
        """
        Process the steps data of the recipe.

        :param builder: Recipe Builder instance.
        """
        steps_data = self.request.POST.get('steps_data')
        if steps_data:
            steps = json.loads(steps_data)
            for step_entry in steps:
                try:
                    builder.build_step(step_entry)
                except Exception as e:
                    logger.error(f"Error adding step '{step_entry}': {e}")

    def process_status(self, builder: NormalRecipeBuilder):
        """
        Process the status data of the recipe.

        :param builder: Recipe Builder instance.
        """
        try:
            is_approved = AIRecipeAdvisor(builder.build_recipe()).recipe_approval()
            if is_approved == 'True':
                builder.build_details(AI_status=True)
            elif is_approved == 'False':
                builder.build_details(AI_status=False)
            builder.build_recipe().save()
        except Recipe.DoesNotExist:
            logger.error(f"Recipe with ID {builder.build_recipe()} does not exist.")
        except Exception as e:
            logger.error(f"Error during recipe approval: {e}")

    def process_nutrition(self, builder: NormalRecipeBuilder):
        """
        Process the nutrition data for the recipe.

        :param builder: Recipe Builder instance.
        """
        try:
            advisor = AIRecipeAdvisor(builder.build_recipe())
            nutrition_data = json.dumps(advisor.nutrition_calculator())
            if nutrition_data:
                nutrition_json = json.loads(nutrition_data)
                nutrients = nutrition_json.get("nutrients", [])
                for nutrition_entry in nutrients:
                    name = nutrition_entry.get("name")
                    amount = nutrition_entry.get("amount")
                    unit = nutrition_entry.get("unit")
                    if name and amount is not None:
                        nutrition_obj, _ = Nutrition.objects.get_or_create(name=name)
                        builder.build_nutrition(
                            nutrition=nutrition_obj,
                            amount=Decimal(amount),
                            unit=unit
                        )
        except Exception as e:
            logger.error(f"Error processing nutrition data: {e}")

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
            return 1, equipment_entry

          
class FavouritePage(generic.ListView):
    """FavouritePage view."""

    model = Favourite
    template_name = "favourite.html"
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


class MyRecipeView(generic.ListView):
    """MyRecipeView view."""

    model = Recipe
    template_name = "my_recipe.html"
    context_object_name = "my_recipes"  # Name for use in the template

    def get_queryset(self):
        """Return user's recipe."""
        return Recipe.objects.filter(poster_id=self.request.user)

    def get_context_data(self, **kwargs):
        """Return context of user's recipe."""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['accept'] = queryset.filter(status=StatusCode.APPROVE.value[0])
        context['reject'] = queryset.filter(status=StatusCode.REJECTED.value[0])
        context['pending'] = queryset.filter(status=StatusCode.PENDING.value[0])
        return context
