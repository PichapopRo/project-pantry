from webpage.models import Recipe, Equipment, Ingredient, RecipeStep, IngredientList, EquipmentList
from django.contrib.auth.models import User
from abc import ABC, abstractmethod


class Builder(ABC):
    """
    Abstract base class for constructing recipe objects.

    This class defines the interface for building various components of a recipe,
    including the recipe itself, its ingredients, required equipment, and steps.
    Concrete implementations must provide specific logic for each method.
    """

    @abstractmethod
    def build_recipe(self) -> Recipe:
        """
        Build and return the main recipe object.

        :return: A Recipe object that represents the constructed recipe.
        """
        pass

    @abstractmethod
    def build_ingredient(self, ingredient: Ingredient, amount: int, unit: str):
        """
        Build and return the ingredients associated with the recipe.

        :param ingredient: The ingredient used in the recipe.
        :param amount: The amount of the ingredient needed in the recipe.
        :param unit: The unit of the ingredient amount eg. Grams, Kg.
        """
        pass

    @abstractmethod
    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build and return the equipment needed for the recipe.

        :param equipment: The equipment used in the recipe.
        :param amount: The amount of the equipment needed in the recipe.
        :param unit: The unit of the equipment amount eg. Grams, spoon.
        """
        pass

    @abstractmethod
    def build_step(self, step: RecipeStep):
        """
        Build the step in the recipe.

        :param step: The step in the recipe.
        """
        pass

    @abstractmethod
    def build_user(self, user: User):
        """
        Build the user which is the author of the recipe.

        :param user: The user that is the author of the recipe.
        """
        pass


class NormalRecipeBuilder(Builder):
    """
    Concrete implementation of Builder for constructing recipes in normal cases.

    This class is responsible for assembling a Recipe object along with its
    associated ingredients and equipment using information from the user.
    """

    def __init__(self, name: str, user: User):
        """
        Initialize the NormalRecipeBuilder instance.

        :param name: The name of the recipe.
        :param user: The user that is the author of the recipe.
        """
        self.__recipe = Recipe.objects.create(name=name, poster_id=user)

    def build_recipe(self) -> Recipe:
        """
        Build and return a standard Recipe object.

        :return: A Recipe object that represents the constructed standard recipe.
        """
        return self.__recipe

    def build_ingredient(self, ingredient: Ingredient, amount: int, unit: str):
        """
        Build and return the ingredients for the standard recipe.

        :param ingredient: The ingredient used in the recipe.
        :param amount: The amount of the ingredient needed in the recipe.
        :param unit: The unit of the ingredient amount eg. Grams, Kg.
        """
        ingredient_list = IngredientList.objects.create(
            ingredient=ingredient,
            recipe=self.__recipe,
            amount=amount,
            unit=unit
        )
        return ingredient_list

    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build the equipment needed for the standard recipe.

        :param equipment: The equipment used in the recipe.
        :param amount: The amount of the equipment needed in the recipe.
        :param unit: The unit of the equipment amount eg. Grams, spoon.
        """
        equipment_list = EquipmentList.objects.create(
            equipment=equipment,
            recipe=self.__recipe,
            amount=amount,
            unit=unit
        )
        return equipment_list

    def build_step(self, step: RecipeStep):
        """
        Build the step in the standard recipe.

        :param step: The step in the recipe.
        """
        step.recipe = self.__recipe
        step.save()

    def build_user(self, user: User):
        """
        Build the user which is the author of the recipe.

        :param user: The user that is the author of the recipe.
        """
        self.__recipe.poster_id = user
        self.__recipe.save()


class SpoonacularRecipeBuilder(Builder):
    """
    Concrete implementation of Builder for constructing recipes from Spoonacular API data.

    This class is responsible for assembling a Recipe object along with its
    associated ingredients and equipment using data retrieved from the Spoonacular API.
    """

    def __init__(self, name: str, user: User):
        """
        Initialize the SpoonacularRecipeBuilder instance.

        :param name: The name of the recipe.
        :param user: The user that is the author of the recipe.
        """
        self.__recipe = Recipe.objects.create(name=name, poster_id=user)

    def build_recipe(self) -> Recipe:
        """
        Return a Recipe object with data from Spoonacular API.

        :return: A Recipe object that represents the constructed recipe based on
        Spoonacular data.
        """
        return self.__recipe

    def build_ingredient(self, ingredient: Ingredient, amount: int, unit: str):
        """
        Build the ingredients for the recipe sourced from Spoonacular API.

        :param ingredient: The ingredient used in the recipe.
        :param amount: The amount of the ingredient needed in the recipe.
        :param unit: The unit of the ingredient amount eg. Grams, Kg.
        """
        ingredient_list = IngredientList.objects.create(
            ingredient=ingredient,
            recipe=self.__recipe,
            amount=amount,
            unit=unit
        )
        return ingredient_list

    def build_step(self, step: RecipeStep):
        """
        Build the step in the Spoonacular recipe.

        :param step: The step in the recipe.
        """
        step.recipe = self.__recipe
        step.save()

    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build the equipment needed for the recipe sourced from Spoonacular API.

        :param equipment: The equipment used in the recipe.
        :param amount: The amount of the equipment needed in the recipe.
        :param unit: The unit of the equipment amount eg. Grams, spoon.
        """
        equipment_list = EquipmentList.objects.create(
            equipment=equipment,
            recipe=self.__recipe,
            amount=amount,
            unit=unit
        )
        return equipment_list

    def build_user(self, user: User):
        """
        Build the user which is the author of the recipe.

        :param user: The user that is the author of the recipe.
        """
        self.__recipe.poster_id = user
        self.__recipe.save()
