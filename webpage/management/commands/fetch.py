"""Module for fetching and storing recipes from the Spoonacular API."""
import time
from django.core.management.base import BaseCommand

from webpage.models import Cuisine
from webpage.modules.proxy import GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')
get_data = GetDataSpoonacular()


class Command(BaseCommand):
    """Command to fetch and store recipes from the Spoonacular API."""

    help = 'Fetch and store all recipes from Spoonacular API'

    def handle(self, *args, **kwargs):
        """
        Fetch recipes from the Spoonacular API and store them using the provided proxy.

        Handle API responses and implement rate limiting.

        :param *args: Positional arguments.
        :param **kwargs: Keyword arguments.
        """
        cuisines = ['Thai', 'Italian', 'Mexican']
        for cuisine in cuisines:
            param = FilterParam(offset=0, number=1, cuisine=cuisine)
            _list = get_data.filter_recipe(param)
            for recipe_data in _list:
                recipe = recipe_data.get_recipe()
                recipe.save()
                cuisine_obj, created = Cuisine.objects.get_or_create(name=cuisine)
                recipe.cuisine.add(cuisine_obj)

                self.stdout.write(self.style.SUCCESS(f"Saved {recipe.name} with cuisine {cuisine}"))
                time.sleep(1)
