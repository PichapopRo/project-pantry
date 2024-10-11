from abc import ABC, abstractmethod
from django.db.models import QuerySet
from webpage.models import Recipe, Equipment, EquipmentList
import requests


class GetData(ABC):
    """
    Abstract base class defining the interface for data retrieval from a recipe API.

    This class serves as a blueprint for concrete implementations that will provide
    methods to find recipes by their ID or name.
    """

    @abstractmethod
    def find_by_id(self, id: int) -> QuerySet[Recipe]:
        """
        Find the recipe using the recipe's id.

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


class GetDataProxy(GetData, ABC):
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

        def find_by_id(self, id: int) -> QuerySet[Recipe]:
            """
            Find the recipe from the API using the recipe's ID.

            This method includes additional logic to save the data (including equipment)
            into the database if the recipe does not exist.

            :param id: The recipe id.
            :return: QuerySet containing the Recipe object.
            """
            recipe_queryset = self._service.find_by_id(id)
            if not recipe_queryset.exists():
                # Retrieve the recipe data from the API
                recipe_data = self._service.find_by_id(id).first()
                if recipe_data:
                    # Save the recipe in the database
                    recipe = Recipe(
                        name=recipe_data.name,
                        spoonacular_id=recipe_data.spoonacular_id,
                        estimated_time=recipe_data.estimated_time,
                        images=recipe_data.images,
                    )
                    recipe.save()

                    # Save the associated equipment in the database
                    for equipment_data in recipe_data.equipment:
                        equipment, created = Equipment.objects.get_or_create(
                            name=equipment_data.name,
                            spoonacular_id=equipment_data.spoonacular_id,
                            defaults={'picture': equipment_data.picture}
                        )
                        # Create the relationship between recipe and equipment
                        EquipmentList.objects.create(
                            equipment=equipment,
                            recipe=recipe,
                            amount=equipment_data.amount,
                            unit=equipment_data.unit
                        )

                    # Return the saved recipe
                    return Recipe.objects.filter(spoonacular_id=recipe.spoonacular_id)
            return recipe_queryset

        def find_by_name(self, name: str) -> QuerySet[Recipe]:
            """
            Find the recipe from the API using the recipe's name.

            :param name: The recipe name.
            :return: QuerySet containing the Recipe object.
            """
            recipe_queryset = self._service.find_by_name(name)
            if not recipe_queryset.exists():
                # Retrieve the recipe data from the API
                recipe_data = self._service.find_by_name(name).first()
                if recipe_data:
                    # Save the recipe in the database
                    recipe = Recipe(
                        name=recipe_data.name,
                        spoonacular_id=recipe_data.spoonacular_id,
                        estimated_time=recipe_data.estimated_time,
                        images=recipe_data.images,
                    )
                    recipe.save()

                    # Save the associated equipment in the database
                    for equipment_data in recipe_data.equipment:
                        equipment, created = Equipment.objects.get_or_create(
                            name=equipment_data.name,
                            spoonacular_id=equipment_data.spoonacular_id,
                            defaults={'picture': equipment_data.picture}
                        )
                        # Create the relationship between recipe and equipment
                        EquipmentList.objects.create(
                            equipment=equipment,
                            recipe=recipe,
                            amount=equipment_data.amount,
                            unit=equipment_data.unit
                        )
                    # Return the saved recipe
                    return Recipe.objects.filter(spoonacular_id=recipe.spoonacular_id)
            return recipe_queryset


class GetDataSpoonacular(GetData):
    """
    Concrete implementation of GetData that interacts with the Spoonacular API.

    This class provides specific methods for retrieving recipes by ID or name
    using Spoonacular's API endpoints.
    """

    def __init__(self):
        self.api_key = 'YOUR_SPOONACULAR_API_KEY'  # Replace with your actual API key
        self.base_url = 'https://api.spoonacular.com/recipes'

    def find_by_id(self, id: int) -> QuerySet[Recipe]:
        """
        Find the recipe from Spoonacular's API using the recipe's ID.

        :param id: The recipe id.
        :return: QuerySet containing the Recipe object corresponding to the provided ID.
        """
        response = requests.get(f'{self.base_url}/{id}/information?apiKey={self.api_key}')
        if response.status_code == 200:
            data = response.json()
            # Create a Recipe object from the API response
            recipe = Recipe(
                name=data['title'],
                spoonacular_id=data['id'],
                estimated_time=data.get('readyInMinutes', 0),
                images=data['image'],
            )
            return Recipe.objects.filter(
                spoonacular_id=recipe.spoonacular_id)
        return Recipe.objects.none()

    def find_by_name(self, name: str) -> QuerySet[Recipe]:
        """
        Find the recipe from Spoonacular's API using the recipe's name.

        :param name: The recipe name.
        :return: QuerySet containing the Recipe object corresponding to the provided name.
        """
        response = requests.get(f'{self.base_url}/search?query={name}&apiKey={self.api_key}')
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                recipe_id = data['results'][0]['id']
                # Use find_by_id to get full details
                return self.find_by_id(recipe_id)
        # Return an empty queryset if no recipes found
        return Recipe.objects.none()
