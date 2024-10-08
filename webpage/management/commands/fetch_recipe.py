import requests
import time
from django.core.management.base import BaseCommand
from webpage.models import Recipe, Ingredient, Equipment, RecipeStep

API_KEY = '8e40e58f1ffd4af39dbce6b302e1f709'


class Command(BaseCommand):
    help = 'Fetch and store all recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        query_params = {
            'apiKey': API_KEY,
            'number': 10,
            # Number of recipes to fetch per request (maximum allowed is 100)
            'offset': 0  # Start with the first page
        }

        while True:
            # Make the API request to fetch a batch of recipes
            url = 'https://api.spoonacular.com/recipes/complexSearch'
            response = requests.get(url, params=query_params)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(
                    f"Failed to fetch data from Spoonacular. Status code: {response.status_code}"))
                break

            data = response.json()
            recipes = data.get('results', [])

            # If no more recipes are returned, we have reached the end of
            # the dataset
            if not recipes:
                self.stdout.write(
                    self.style.SUCCESS("All recipes fetched successfully."))
                break

            # Process and save each recipe
            for recipe_summary in recipes:
                recipe_id = recipe_summary['id']
                self.fetch_and_save_recipe(recipe_id)

            # Increment offset to fetch the next batch of recipes
            query_params['offset'] += query_params['number']

            # Respect API rate limits (adjust this based on your API limits)
            time.sleep(1)  # Wait 1 second before making the next request

    def fetch_and_save_recipe(self, recipe_id):
        # Fetch detailed information for the recipe
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        response = requests.get(url, params={'apiKey': API_KEY})

        if response.status_code == 200:
            data = response.json()
            self.save_recipe(data)
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to fetch recipe {recipe_id}'))

    def save_recipe(self, data):
        # Save the recipe
        recipe, created = Recipe.objects.get_or_create(
            spoonacular_id=data['id'],
            defaults={'name': data['title']}
        )

        # Save the ingredients
        for ingredient_data in data['extendedIngredients']:
            ingredient, created = Ingredient.objects.get_or_create(
                spoonacular_id=ingredient_data['id'],
                defaults={'name': ingredient_data['name'],
                          'picture': ingredient_data['image']}
            )
            recipe.ingredients.add(ingredient)

        # Save the equipment (if available)
        for equipment_data in data.get('equipment', []):
            equipment, created = Equipment.objects.get_or_create(
                spoonacular_id=equipment_data['id'],
                defaults={'name': equipment_data['name'],
                          'picture': equipment_data['image']}
            )
            recipe.equipment.add(equipment)

        # Save the steps
        if data.get('analyzedInstructions'):
            for step_data in data['analyzedInstructions'][0]['steps']:
                step, created = RecipeStep.objects.get_or_create(
                    number=step_data['number'],
                    description=step_data['step'],
                    recipe=recipe
                )
                recipe.steps.add(step)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully saved recipe: {recipe.name}'))
