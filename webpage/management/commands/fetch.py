"""Module for fetching and storing recipes from the Spoonacular API."""
import time
from django.core.management.base import BaseCommand
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')
proxy = GetDataProxy(GetDataSpoonacular())


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
        param = FilterParam(
            offset = 66,
            number = 3
        )
        _list = proxy.filter_recipe(param)
        for recipe in _list:
            self.stdout.write(self.style.SUCCESS(f"Save {recipe.name} successfully."))
            recipe.get_recipe().save()
            
        self.stdout.write(self.style.SUCCESS("All recipes fetched successfully."))

        param.offset += param.number
        time.sleep(1)  # Respect API rate limits
