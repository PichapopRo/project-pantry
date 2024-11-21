"""This module saves the data fetched from the API into the database if it doesn't exists."""

from typing import Any
from abc import ABC, abstractmethod
from django.db.models import QuerySet
from webpage.models import Recipe
import requests
from decouple import config
from webpage.modules.filter_objects import FilterParam
from webpage.modules.recipe_facade import RecipeFacade
from webpage.modules.builder import SpoonacularRecipeBuilder
import logging
API_KEY = config('API_KEY', default=None)
logger = logging.getLogger("proxy class")


class GetData(ABC):
    """
    Abstract base class defining the interface for data retrieval from a recipe API.

    This class serves as a blueprint for concrete implementations that will provide
    methods to find recipes by their ID or name.
    """
    
    @abstractmethod
    def find_by_spoonacular_id(self, id: int) -> Recipe:
        """
        Find the recipe using the recipe's spooacular_id.

        :param id: The recipe id.
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
    
    @classmethod
    @abstractmethod
    def convert_parameter(cls, param: FilterParam) -> Any:
        """
        Deals with converting the FilterParam class's parameter into the one that class can use.
        
        :param param: The FilterParam class that you want to convert.
        :return: The parameter that the class can use.
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
    
    def find_by_spoonacular_id(self, id: int) -> Recipe | None:
        """
        Find the recipe using the recipe's spoonacular_id.

        This method includes additional logic to save the data (including equipment)
        into the database if the recipe does not exist.

        :param id: The recipe spoonacular_id.
        :return: The Recipe object with the specified ID, return None if not found.
        """
        recipe_queryset: QuerySet = Recipe.objects.filter(spoonacular_id=id)
        if not recipe_queryset.exists():
            # Retrieve the recipe data from the API
            spoonacular_recipe_queryset = self._service.find_by_spoonacular_id(id)
            return spoonacular_recipe_queryset
        return recipe_queryset.first()

    def filter_recipe(self, param: FilterParam) -> list[RecipeFacade]:
        """
        Filter the recipe.

        :param param: The filter parameter object.
        :return: List with RecipeFacade representing the recipe.
        """
        queryset = Recipe.objects.all()
        for _filter in self.convert_parameter(param):
            key: str = list(_filter.keys())[0]
            if _filter[key] == "" or _filter[key] is None:
                continue
            _dict = {key: _filter[key]}
            queryset = queryset.filter(**_dict)
        logger.debug(queryset)

        start = param.offset - 1
        stop = start + param.number
        logger.debug(f"the len of the queryset is {len(queryset)}")

        if len(queryset) < param.offset:
            # If the offset is greater than the number of records in the database, 
            # skip the database part entirely
            initial_list = []
            remaining_number = param.number
        else:
            initial_list = list(queryset[start:stop])
            remaining_number = param.number - len(initial_list)

        if remaining_number > 0:
            param.offset = 1
            param.number = remaining_number
            logger.debug(f"param sent to the service: {param}")
            later_part = self._service.filter_recipe(param)
            logger.debug(later_part)
        else:
            later_part = []

        _list = []
        for recipe in initial_list:
            facade = RecipeFacade()
            facade.set_recipe(recipe)
            _list.append(facade)

        return _list + later_part
    
    @classmethod
    def convert_parameter(cls, param: FilterParam) -> list[dict[str, str]]:
        """
        Convert the FilterParam class into Django filter.
        
        :param param: The FilterParam class that you want to convert.
        :return: The list of a dictionaries containing one pair of key and value.
        """
        parameter_for_django = []
        _keys = {
            'includeIngredients': 'ingredientlist__ingredient__name__icontains',
            "diet": 'diets__name__icontains',
            'maxReadyTime': 'estimated_time__lte',
            'titleMatch': 'name__contains'
        }
        parameter_from_object = param.get_param()
        for key in parameter_from_object:
            if isinstance(parameter_from_object[key], list):
                for value in parameter_from_object[key]:
                    parameter_for_django.append({_keys[key]: value})
            else:
                parameter_for_django.append({_keys[key]: parameter_from_object[key]})
        return parameter_for_django


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
        
    def find_by_spoonacular_id(self, id: int) -> Recipe:
        """
        Find the recipe from Spoonacular's API using the recipe's spoonacular_id.

        :param id: The Spooacular recipe id.
        :return: QuerySet containing the Recipe object corresponding to the provided ID.
                 Raise an Exeption if the recipe cannot found.
        """
        builder = SpoonacularRecipeBuilder(name="", spoonacular_id=id)
        builder.build_name()
        builder.build_ingredient()
        builder.build_equipment()
        builder.build_nutrition()
        builder.build_step()
        builder.build_details()
        builder.build_diet()
        builder.build_spoonacular_id()
        builder.build_recipe().save()
        return builder.build_recipe()
    
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
        query_params.update(self.convert_parameter(param))
        
        response = requests.get(self.__complex_url, params=query_params)

        if response.status_code != 200:
            logger.debug("Response code: ", response.status_code)
            if response.status_code != 402:
                raise Exception("Error code: ", response.status_code)
            logger.warning("You ran out of quota.")
        
        data = response.json()
        recipes = data.get('results', [])

        if not recipes:
            pass
        
        _list: list[RecipeFacade] = []
        for recipe in recipes:
            recipe_facade = RecipeFacade()
            recipe_facade.set_by_spoonacular(
                name=recipe["title"],
                _id=recipe["id"],
                image=recipe["image"]
            )
            _list.append(recipe_facade)
            
        return _list
    
    @classmethod
    def convert_parameter(cls, param: FilterParam) -> Any:
        """
        Deals with converting the FilterParam class's parameter into the one that class can use.
        
        :param param: The FilterParam class that you want to convert.
        :return: The parameter that the class can use.
        """
        parameter_from_object = param.get_param()
        for key in parameter_from_object:
            if isinstance(parameter_from_object[key], list):
                parameter_from_object[key] = ','.join(parameter_from_object[key])
        return parameter_from_object
