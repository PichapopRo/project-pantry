"""Provide a facade for the SpoonacularRecipeBuilder and Recipe."""

from webpage.models import Recipe


class RecipeFacade():  # Shot gun
    """
    A facade class that will handle the building recipe process.
    
    :param image: The image URL
    :param name: The name of the recipe
    :param id: The Spoonacular ID of the recipe, None if there's none.
    :param favou rite: The number of people who put the recipe in their favorite.
    :param pk: The pk of the recipe. It is None if the recipe comes from Spoonacular.
    :param username: The username of the poster of this recipe.
    :param number_id: The unique identifier of each stuffs things.
    """
    
    def __init__(self, number_id: int):
        """Initialize the class."""
        self.__recipe: Recipe | None = None
        self.favourite: int
        self.pk: int|None = None
        self.username: str
        self.number_id: int = number_id
    
    def set_recipe(self, recipe: Recipe):
        """
        Set up the class using already-existing recipe.
        
        :param recipe: The recipe to be used in the facade.
        """
        self.__recipe = recipe
        self.image = recipe.image
        self.name = recipe.name
        self.spoonacular_id = recipe.spoonacular_id
        self.favourite = recipe.favourites
        self.pk = recipe.id
        self.username = recipe.poster_id.username
    
    def set_by_spoonacular(self, name: str, _id: str, image: str | None):
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
        self.username = "Spoonacular"
        
    def get_recipe(self) -> Recipe | None:
        """
        Get the recipe class.
        
        :return: The recipe that you are dealing with.
                    Returns None if it cannot find the recipe with that id.
        """
        if self.__recipe is not None:
            return self.__recipe
        if self.id is None and self.pk is None:
            raise Exception("Please set something")
        from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
        proxy = GetDataProxy(GetDataSpoonacular())
        return proxy.find_by_spoonacular_id(self.id)
    
    def __str__(self):
        """Return the string representation of the object."""
        return f"Recipe name: {self.name}, Recipe ID: {self.id}"
