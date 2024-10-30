from abc import ABC, abstractmethod
from webpage.modules.builder import SpoonacularRecipeBuilder
from webpage.models import Recipe

class RecipeFacade(): # Quite a bad code, fix later.
    """
    A facade class that will handle the building recipe process.
    """
    
    def __init__(self):
        self.__recipe: Recipe|None = None
    
    def set_recipe(self, recipe: Recipe):
        self.__recipe = recipe
    
    def set_by_spoonacular(self, name: str, id:str, picture: str|None):
        self.__recipe = None
        self.picture = picture
        self.name = name
        self.id = id
        
    def get_recipe(self) -> Recipe:
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
    
    