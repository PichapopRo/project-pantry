"""This module saves the data fetched from the API into the database if it doesn't exists."""

from abc import ABC, abstractmethod
from django.db.models import QuerySet
from webpage.models import Recipe
import requests
from decouple import config
from webpage.modules.filter_objects import FilterParam
from webpage.modules.recipe_facade import RecipeFacade
import logging
API_KEY = config('API_KEY')
logger = logging.getLogger("proxy class")


class GetData(ABC):
    """
    Abstract base class defining the interface for data retrieval from a recipe API.

    This class serves as a blueprint for concrete implementations that will provide
    methods to find recipes by their ID or name.
    """

    @abstractmethod
    def find_by_name(self, name: str) -> list[RecipeFacade]:
        """
        Find the recipe using the recipe's name.

        :param name: The recipe name.
        :return: A list containing the RecipeFacade object.
        """
        pass
    
    @abstractmethod
    def filter_recipe(self, param: FilterParam) -> list[RecipeFacade]:
        """
        Filter the recipe.
        
        :param param: The filter parameter object.
        :return: List with RecipeFacade representing the recipe.
        """
        pass


class GetDataProxy(GetData):
    """
    Proxy class that controls access to the underlying GetData service.

    This class adds a layer of abstraction, allowing for operations
    such as saving data into the database when retrieving recipes that do not
    exist in the database from the API.
    """

    def __init__(self, service: GetData):
        """
        Initialize with a specific service instance for data retrieval.

        :param service: An instance of a class that implements the GetData interface.
        """
        self._service = service

    def find_by_name(self, name: str) -> list[RecipeFacade]:
        """
        Find the recipe from the API using the recipe's name.

        :param name: The recipe name.
        :return: A list containing the RecipeFacade object. Returns an empty list if
                    the it cannot find the result.
        """
        _list = []
        recipe_queryset = Recipe.objects.filter(name__contains=name)
        if not recipe_queryset.exists():
            # Retrieve the recipe data from the API
            spoonacular_recipe_queryset = self._service.find_by_name(name)
            return spoonacular_recipe_queryset
        for recipe in recipe_queryset:
            facade = RecipeFacade()
            facade.set_recipe(recipe)
            _list.append(facade)
        return _list

    def filter_recipe(self, param: FilterParam) -> list[RecipeFacade]:
        """
        Filter the recipe.
        
        :param param: The filter parameter object.
        :return: List with RecipeFacade representing the recipe.
        """
        queryset = Recipe.objects.all()
        for _filter in param.get_param():
            if param.get_param()[_filter] == "" or param.get_param()[_filter] is None:
                continue
            _dict = {
                self._service.get_django_filter(_filter): param.get_param()[_filter]
            }
            queryset = queryset.filter(**_dict)
        
        stop = 0
        start = 0
        later_part = []
        if len(queryset) < param.number + param.offset - 1:
            stop = len(queryset)
            start = param.offset
            param.number = param.number - len(queryset)
            param.offset = 1
            later_part = self._service.filter_recipe(param)
        else:
            stop = param.number + param.offset - 1
            start = param.offset
        _list = []
        logger.debug(f"param.number: {start}, number: {stop}")
        for recipe in queryset[start - 1: stop]:
            facade = RecipeFacade()
            facade.set_recipe(recipe)
            _list.append(facade)
        return _list + later_part

    def filter_by_difficulty(self, difficulty: str) -> QuerySet:
        """
        Filter recipes by difficulty using the `get_difficulty` method.

        :param difficulty: The difficulty to filter by.
        :return: A filtered queryset of recipes.
        """
        recipes = self._queryset.all()
        filtered_recipes = [recipe for recipe in recipes if recipe.get_difficulty() == difficulty]
        return Recipe.objects.filter(id__in=[recipe.id for recipe in filtered_recipes])


class GetDataSpoonacular(GetData):
    """
    Concrete implementation of GetData that interacts with the Spoonacular API.

    This class provides specific methods for retrieving recipes by ID or name
    using Spoonacular's API endpoints.
    """

    def __init__(self):
        """Initialize API_KEY and base_url."""
        self.api_key = API_KEY  # Replace with your actual API key
        self.base_url = 'https://api.spoonacular.com/recipes'
        self.__complex_url = 'https://api.spoonacular.com/recipes/complexSearch'

    def find_by_name(self, name: str) -> list[RecipeFacade]:
        """
        Find the recipe from Spoonacular's API using the recipe's name.

        :param name: The recipe name.
        :return: A list containing the RecipeFacade object corresponding to the provided name.
                 Returns an empty list if cannot find any recipe.
        """
        response = requests.get(f'{self.base_url}/search?query={name}&apiKey={self.api_key}')
        if response.status_code == 200:
            data: dict = response.json()
            _return_list = []
            recipes = data.get('results', [])
            for recipe in recipes:
                facade = RecipeFacade()
                facade.set_by_spoonacular(
                    name=recipe["name"],
                    id=recipe['id'],
                    image=recipe["image"]
                )
                _return_list.append(facade)

            return _return_list

        # Return an empty list if no recipes found
        return []
    
    def filter_recipe(self, param: FilterParam) -> list[RecipeFacade]:
        """
        Filter the recipe.
        
        :param param: The filter parameter object.
        :return: List with RecipeFacade representing the recipe.
                    Returns an empty list if it cannot find the recipe.
        """
        query_params: dict[str, str | int | bool | list] = {
            'apiKey': API_KEY,
            'number': param.number,
            'offset': param.offset
        }
        query_params.update(param.get_param())
        
        print(query_params)
        
        response = requests.get(self.__complex_url, params=query_params)

        if response.status_code != 200:
            raise Exception("Cannot retrieve the information")
        
        data = response.json()
        recipes = data.get('results', [])

        if not recipes:
            raise Exception("Cannot find the recipe")
        
        _list: list[RecipeFacade] = []
        for recipe in recipes:
            recipe_facade = RecipeFacade()
            recipe_facade.set_by_spoonacular(
                name=recipe["title"],
                id=recipe["id"],
                image=recipe["image"]
            )
            _list.append(recipe_facade)
            
        return _list
    
    @classmethod
    def get_django_filter(cls, param_name: str):
        """
        Get the Django filter parameter key from Spoonacular filter parameter key.
        
        :param param_name: The name (or key) of the Spoonacular parameter.
        :return: The name (or key) of the Django filter parameter.
        """
        _keys = {
            'includeIngredients': 'ingredientlist__ingredient__name__icontains',
            'equipment': 'equipmentlist__equipment__name__icontains',
            "diet": 'diets__name__icontains',
            'maxReadyTime': 'estimated_time__lte',
            'titleMatch': 'name__contains'
        }
        return _keys[param_name]
