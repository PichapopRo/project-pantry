from io import StringIO
import requests
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from webpage.models import Recipe, Ingredient, Equipment, RecipeStep
from webpage.modules.builder import SpoonacularRecipeBuilder
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')

class Command(BaseCommand):    
    help = 'Fetch and store all recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        query_params = {
            'apiKey': API_KEY,
            'number': 10,
            'offset': 0
        }

        url = 'https://api.spoonacular.com/recipes/complexSearch'
        response = requests.get(url, params=query_params)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(
                f"Failed to fetch data from Spoonacular. Status code: {response.status_code}"))
            return

        data = response.json()
        recipes = data.get('results', [])

        if not recipes:
            self.stdout.write(self.style.SUCCESS("All recipes fetched successfully."))
            return

        for recipe_summary in recipes:
            recipe_id = recipe_summary['id']
            builder = SpoonacularRecipeBuilder(
                spoonacular_id=recipe_summary['id'],
                name = recipe_summary['title']
                )
            builder.build_ingredient()
            builder.build_equipment()
            builder.build_step()
            builder.build_recipe().save()
            self.stdout.write(self.style.SUCCESS(f"Save {recipe_summary['title']} successfully."))

        query_params['offset'] += query_params['number']
        time.sleep(1)  # Respect API rate limits

