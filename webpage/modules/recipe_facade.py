"""Provide a facade for the SpoonacularRecipeBuilder and Recipe."""

from webpage.models import Recipe


class RecipeFacade():  # Shot gun
    """
    A facade class that will handle the building recipe process.
    
    :param image: The image URL
    :param name: The name of the recipe
    :param id: The Spoonacular ID of the recipe, None if there's none.
    :param favorite: The number of people who put the recipe in their favorite.
    """
    
    def __init__(self):
        """Initialize the class."""
        self.__recipe: Recipe | None = None
        self.image = None
        self.name = None
        self.id = None
        self.favorite = None
    
    def set_recipe(self, recipe: Recipe):
        """
        Set up the class using already-existing recipe.
        
        :param recipe: The recipe to be used in the facade.
        """
        self.__recipe = recipe
        self.image = recipe.image
        self.name = recipe.name
        self.id = recipe.spoonacular_id
        self.favorite = recipe.favourites
    
    def set_by_spoonacular(self, name: str, _id: int, image: str | None):
        """
        Set up the class using newly-fetched recipe.
        
        :param name: The recipe name.
        :param _id: The recipe's id.
        :param image: The url of the recipe's image.
        """
        self.__recipe = None
        self.image = image
        self.name = name
        self.id = _id
        self.favorite = 0
        
    def get_recipe(self) -> Recipe | None:
        """
        Get the recipe class.
        
        :return: The recipe that you are dealing with.
                    Returns None if it cannot find the recipe with that id.
        """
        if self.__recipe is not None:
            return self.__recipe
        if self.id is None:
            raise Exception("Please set something")
        from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
        proxy = GetDataProxy(GetDataSpoonacular())
        return proxy.find_by_spoonacular_id(self.id)
    
    def __str__(self):
        """Return the string representation of the object."""
        return f"Recipe name: {self.name}, Recipe ID: {self.id}"
