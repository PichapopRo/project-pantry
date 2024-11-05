"""Provide a facade for the SpoonacularRecipeBuilder and Recipe."""

from webpage.modules.builder import SpoonacularRecipeBuilder
from webpage.models import Recipe


class RecipeFacade():  # Shot gun
    """A facade class that will handle the building recipe process."""
    
    def __init__(self):
        """Initialize the class."""
        self.__recipe: Recipe | None = None
    
    def set_recipe(self, recipe: Recipe):
        """
        Set up the class using already-existing recipe.
        
        :param recipe: The recipe to be used in the facade.
        """
        self.__recipe = recipe
        self.image = recipe.image
        self.name = recipe.name
        self.id = recipe.spoonacular_id
    
    def set_by_spoonacular(self, name: str, id: str, image: str | None):
        """
        Set up the class using newly-fetched recipe.
        
        :param name: The recipe name.
        :param id: The recipe's id.
        :param image: The url of the recipe's image.
        """
        self.__recipe = None
        self.image = image
        self.name = name
        self.id = id
        
    def get_recipe(self) -> Recipe:
        """
        Get the recipe class.
        
        :return: The recipe that you are dealing with.
        """
        if self.__recipe is not None:
            return self.__recipe
        if self.id is not None:
            raise Exception("Please set something")
        builder = SpoonacularRecipeBuilder(name=self.name, spoonacular_id=id)
        builder.build_diet()
        builder.build_ingredient()
        builder.build_details()
        builder.build_equipment()
        builder.build_step()
        builder.build_nutrition()
        return builder.build_recipe()
    
    def __str__(self):
        """Return the string representation of the object."""
        return f"Recipe name: {self.name}, Recipe ID: {self.id}"
