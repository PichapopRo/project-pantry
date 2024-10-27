"""Module for fetching and storing recipes from the Spoonacular API."""
import requests
import time
from django.core.management.base import BaseCommand
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')
proxy = GetDataProxy(GetDataSpoonacular())


class Command(BaseCommand):
    """Command to fetch and store recipes from the Spoonacular API."""

    help = 'Fetch and store all recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.

        Fetches recipes from the Spoonacular API and stores them using
        the provided proxy. This method handles API responses and
        implements rate limiting.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        query_params = {
            'apiKey': API_KEY,
            'number': 10,
            'offset': 50,
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
            proxy.find_by_spoonacular_id(int(recipe_summary['id']))
            self.stdout.write(self.style.SUCCESS(f"Save {recipe_summary['title']} successfully."))

        query_params['offset'] += query_params['number']
        time.sleep(1)  # Respect API rate limits
