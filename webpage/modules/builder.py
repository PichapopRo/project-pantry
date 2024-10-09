from webpage.models import Recipe, Equipment, Ingredient, RecipeStep
from django.contrib.auth.models import User
from abc import ABC

class Builder(ABC):
    """ 
    Abstract base class for constructing recipe objects.

    This class defines the interface for building various components of a recipe, 
    including the recipe itself, its ingredients, required equipment and steps. 
    Concrete implementations must provide specific logic for each method.
    """
    def build_recipe(self):
        """
        Build and return the main recipe object.

        :return: A Recipe object that represents the constructed recipe.
        """
        pass
    
    def build_ingredient(self, ingredient: Ingredient, amount: int, unit: str):
        """
        Build and return the ingredients associated with the recipe.

        :return: A list or collection of Ingredient objects.
        """
        pass
    
    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build and return the equipment needed for the recipe.

        :return: A list or collection of Equipment objects.
        """
        pass


class NormalRecipeBuilder(Builder):
    """ 
    Concrete implementation of Builder for constructing recipes in the normal cases.

    This class is responsible for assembling a Recipe object along with its 
    associated ingredients and equipment using information from the user.
    """
    def __init__(self):
        """
        Initialize the NormalRecipeBuilder instance.
        
        This may include setting up any necessary state or configuration.
        """
        self.__recipe = Recipe.objects.create(name="")
    
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
        pass
    
    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build the equipment needed for the standard recipe.

        :param equipment: The equipment used in the recipe.
        :param amount: The amount of the equipment needed in the recipe.
        :param unit: The unit of the equipment amount eg. Grams, spoon.
        """
        pass
    
    def build_step(self, step: RecipeStep):
        """
        Build the step in the standard recipe.

        :param step: The step in the recipe.
        """
        pass
    
    def build_user(self, user: User):
        """
        Build the user which is the author of the recipe.
        
        :param user: The user that is the author of the recipe.
        """
        pass
    

class SpoonacularRecipeBuilder(Builder):
    """ 
    Concrete implementation of Builder for constructing recipes from Spoonacular API data.

    This class is responsible for assembling a Recipe object along with its 
    associated ingredients and equipment using data retrieved from the Spoonacular API.
    """
    def __init__(self):
        """
        Initialize the SpoonacularRecipeBuilder instance.

        This may include setting up any necessary state or configuration specific to 
        interacting with the Spoonacular API.
        """
        self.__recipe = Recipe.objects.create(name="")
        pass
    
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
        pass
    
    def build_step(self, step: RecipeStep):
        """
        Build the step in the Spoonacular recipe.

        :param step: The step in the recipe.
        """
        pass
    
    def build_equipment(self, equipment: Equipment, amount: int, unit: str):
        """
        Build the equipment needed for the recipe sourced from Spoonacular API.

        :param equipment: The equipment used in the recipe.
        :param amount: The amount of the equipment needed in the recipe.
        :param unit: The unit of the equipment amount eg. Grams, spoon.
        """
        pass
    