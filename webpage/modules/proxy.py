"""These classes may not be used in iteration 1."""

from abc import ABC, abstractmethod
from django.db.models import QuerySet
from webpage.models import Recipe
import requests
from webpage.modules.builder import SpoonacularRecipeBuilder
from decouple import config
API_KEY = config('API_KEY')


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
    def find_by_name(self, name: str) -> QuerySet[Recipe]:
        """
        Find the recipe using the recipe's name.

        :param name: The recipe name.
        """
        pass


class GetDataProxy(GetData):
    """
    Proxy class that controls access to the underlying GetData service.

    This class adds a layer of abstraction, allowing for operations
    such as saving data into the database when retrieving recipes that do not
    exist in the database from the API.
    """

    def __init__(self, service: GetData, queryset: QuerySet):  # bad code
        """
        Initialize with a specific service instance for data retrieval.

        :param service: An instance of a class that implements the GetData interface.
        """
        self._service = service
        self._queryset = queryset

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

    def find_by_name(self, name: str) -> QuerySet[Recipe]:
        """
        Find the recipe from the API using the recipe's name.

        :param name: The recipe name.
        :return: QuerySet containing the Recipe object.
        """
        recipe_queryset = Recipe.objects.filter(name__contains=name)
        if not recipe_queryset.exists():
            # Retrieve the recipe data from the API
            spoonacular_recipe_queryset = self._service.find_by_name(name)
            return spoonacular_recipe_queryset
        return recipe_queryset

    def filter_by_diet(self, diet: str) -> QuerySet:
        """
        Filter recipes based on a diet type (e.g., 'vegan', 'vegetarian').

        :param diet: The diet to filter recipes by.
        :return: A filtered queryset of recipes.
        """
        return self._queryset.filter(diets__name__icontains=diet)

    def filter_by_ingredient(self, ingredient: str) -> QuerySet:
        """
        Filter recipes by a specific ingredient.

        :param ingredient: The ingredient to filter recipes by.
        :return: A filtered queryset of recipes.
        """
        return self._queryset.filter(
            ingredientlist__ingredient__name__icontains=ingredient.lower())

    def filter_by_max_cooking_time(self, estimated_time: int) -> QuerySet:
        """
        Filter recipes by a maximum cooking time (in minutes).

        :param estimated_time: Estimated cooking time in minutes.
        :return: A filtered queryset of recipes.
        """
        return self._queryset.filter(estimated_time__lte=estimated_time)

    def filter_by_equipment(self, equipment_name: str) -> QuerySet:
        """
        Filter recipes by required equipment.

        :param equipment_name: The name of the equipment to filter by.
        :return: A filtered queryset of recipes.
        """
        return self._queryset.filter(equipmentlist__equipment__name__icontains=equipment_name)

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
        builder.build_spoonacular_id()
        builder.build_recipe().save()
        return builder.build_recipe()

    def find_by_name(self, name: str) -> list[SpoonacularRecipeBuilder]:
        """
        Find the recipe from Spoonacular's API using the recipe's name.

        :param name: The recipe name.
        :return: QuerySet containing the Recipe object corresponding to the provided name.
                 Returns an empty list if cannot find any recipe.
        """
        response = requests.get(f'{self.base_url}/search?query={name}&apiKey={self.api_key}')
        if response.status_code == 200:
            data: dict = response.json()
            _return_list = []
            recipes = data.get('results', [])
            for recipe_summary in recipes:
                builder = SpoonacularRecipeBuilder(
                    spoonacular_id=recipe_summary['id'],
                    name=recipe_summary['title']
                )
                builder.build_ingredient()
                builder.build_equipment()
                builder.build_step()
                builder.build_nutrition()
                builder.build_details()
                _return_list.append(builder.build_recipe().save())

            return _return_list

        # Return an empty list if no recipes found
        return []
