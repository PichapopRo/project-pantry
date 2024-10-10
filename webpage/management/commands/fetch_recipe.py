import requests
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from webpage.models import Recipe, Ingredient, Equipment, RecipeStep

API_KEY = 'API KEY'
MAX_RECIPES_TO_FETCH = 10  # Adjust this value as needed


class Command(BaseCommand):
    help = 'Fetch and store all recipes from Spoonacular API (limited)'

    def handle(self, *args, **kwargs):
        query_params = {
            'apiKey': API_KEY,
            'number': MAX_RECIPES_TO_FETCH,
            'offset': 0
        }

        recipes_fetched = 0
        while recipes_fetched < MAX_RECIPES_TO_FETCH:
            url = 'https://api.spoonacular.com/recipes/complexSearch'
            response = requests.get(url, params=query_params)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(
                    f"Failed to fetch data from Spoonacular. Status code: {response.status_code}"))
                break

            data = response.json()
            recipes = data.get('results', [])

            if not recipes:
                self.stdout.write(
                    self.style.SUCCESS(f"Fetched {recipes_fetched} recipes (reached limit)."))
                break

            for recipe_summary in recipes:
                recipe_id = recipe_summary['id']

                # Check if recipe already exists before fetching details
                if not Recipe.objects.filter(spoonacular_id=recipe_id).exists():
                    self.fetch_and_save_recipe(recipe_id)
                    recipes_fetched += 1

                if recipes_fetched >= MAX_RECIPES_TO_FETCH:
                    break  # Stop fetching recipes if limit is reached

            query_params['offset'] += query_params['number']
            time.sleep(1)  # Respect API rate limits

    def fetch_and_save_recipe(self, recipe_id):
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        response = requests.get(url, params={'apiKey': API_KEY})

        if response.status_code == 200:
            data = response.json()
            self.save_recipe(data)
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to fetch recipe {recipe_id}'))

    def save_recipe(self, data):
        # Fetch or create a user (assuming you want to use the first user
        # for all recipes)
        try:
            user, created = User.objects.get_or_create(username='Spoonacular')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create or retrieve user: {e}'))
            return

        # Create the Recipe object associated with the user
        recipe = Recipe.objects.create(
            spoonacular_id=data['id'],
            name=data['title'],
            poster_id=user  # Explicitly assign the user object
        )

        # Save the ingredients
        for ingredient_data in data['extendedIngredients']:
            ingredient, created = Ingredient.objects.get_or_create(
                spoonacular_id=ingredient_data['id'],
                defaults={'name': ingredient_data['name'],
                          'picture': ingredient_data['image']}
            )
            if ingredient:
                recipe.ingredients.add(ingredient)

        # Save the equipment (if available)
        for equipment_data in data.get('equipment', []):
            equipment, created = Equipment.objects.get_or_create(
                spoonacular_id=equipment_data['id'],
                defaults={'name': equipment_data['name'],
                          'picture': equipment_data['image']}
            )
            # Only add the equipment to the recipe if it was successfully
            # retrieved or created
            if equipment:
                recipe.equipment.add(equipment)

        # Save the steps
        if data.get('analyzedInstructions'):
            for step_data in data['analyzedInstructions'][0]['steps']:
                step, created = RecipeStep.objects.get_or_create(
                    number=step_data['number'],
                    description=step_data['step'],
                    recipe=recipe
                )
                # Only add the step if it was successfully retrieved or created
                if step:
                    recipe.steps.add(step)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully saved recipe: {recipe.name}'))