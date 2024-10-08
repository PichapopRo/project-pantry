from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    """An r contains the name, a spoonacauar_id(if exitst) and a link to a picture."""
    name = models.CharField(max_length=100, default='Unnamed Ingredient')
    spoonacular_id = models.IntegerField(unique=True, null=True)
    picture = models.URLField(default='', null=True)

    def __str__(self):
        """Return the ingredient name."""
        return self.name
    

class Equipment(models.Model):
    """An equipment contains the name, a spoonacauar_id(if exitst) and a link to a picture."""
    name = models.CharField(max_length=100, default='Unnamed Equipment')
    spoonacular_id = models.IntegerField(unique=True, default=0)
    picture = models.URLField(default='')

    def __str__(self):
        """Return the equipment name."""
        return self.name


class RecipeStep(models.Model):
    """A recipe's step contain each cooking step of the recipe."""
    number = models.IntegerField(default=1)
    description = models.TextField(default='No description provided')
    recipe = models.ForeignKey('Recipe', related_name='steps', on_delete=models.CASCADE)

    def __str__(self):
        """
        Return the string containing the number of the recipe
        and the description.
        """
        return f'Step {self.number}: {self.description[:50]}'


class Recipe(models.Model):
    """
    The recipe class containg the information about the recipe
    and methods.
    """
    name = models.CharField(max_length=200, default='Unnamed Recipe')
    spoonacular_id = models.IntegerField(unique=True, null=True)
    estimated_time = models.FloatField(default=0)
    images = models.ImageField(upload_to='recipe_images/', blank=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """
        Return the name of the recipe
        
        :return: A string of name.
        """
        return self.name
    
    def get_difficulty(self) -> str:
        """
        Return the dificulty of the recipe.
        
        :return: the difficulty
        """
        #TODO Decide on the difficulity rule. 
        return ""
    
    def get_ingredients() -> list[Ingredient]:
        """Return a list of ingredients of the recipe.
        
        :return: A list of ingredients.
        """
        
    
    def get_equipement() -> list[Ingredient]:
        """Return a list of ingredients of the recipe.
        
        :return: A list of ingredients..
        """
        pass 
    

class IngredientsList(models.Model):
    """The relations representing which ingredient is used in which recipe."""
    ingredients_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=0)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=100)
    
    
class EquipmentList(models.Model):
    """The relations representing which equipment is used in which recipe."""
    equipment_id = models.ForeignKey(Equipment, on_delete=models.CASCADE, default=0)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=100, default="piece")
