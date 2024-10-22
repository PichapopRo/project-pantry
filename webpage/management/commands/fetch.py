from io import StringIO
import requests
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from webpage.models import Recipe, Ingredient, Equipment, RecipeStep
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular

from webpage.modules.builder import SpoonacularRecipeBuilder
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')
proxy = GetDataProxy(GetDataSpoonacular())

class Command(BaseCommand):
    help = 'Fetch and store all recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        query_params = {
            'apiKey': API_KEY,
            'number': 50,
            'offset': 0
        }

        url = 'https://api.spoonacular.com/recipes/complexSearch'
        response = requests.get(url, params=query_params)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(
                f"Failed to fetch data from Spoonacular. Status code: {response.status_code}"))
            return

        data = response.json()
        recipe_ids = [recipe['id'] for recipe in data.get('results', [])]

        # Fetch details for all recipe IDs at once
        detail_url = 'https://api.spoonacular.com/recipes/informationBulk'
        detail_response = requests.get(detail_url,
                                       params={'ids': ','.join(map(str, recipe_ids)),
                                               'apiKey': API_KEY})

        if detail_response.status_code != 200:
            self.stdout.write(self.style.ERROR(
                f"Failed to fetch recipe details. Status code: {detail_response.status_code}"))
            return

        detailed_recipes = detail_response.json()
        for detailed_recipe in detailed_recipes:
            proxy.find_by_spoonacular_id(detailed_recipe['id'])
            self.stdout.write(
                self.style.SUCCESS(f"Saved {detailed_recipe['title']} successfully."))

        query_params['offset'] += query_params['number']
        time.sleep(1)  # Respect API rate limits
