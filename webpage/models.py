from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone

class Ingredient(models.Model):
    """An ingredient contains the name, a spoonacauar_id(if exists) and a link to a picture."""
    name = models.CharField(max_length=100, default='Unnamed Ingredient')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    picture = models.URLField(default='', null=True)

    def __str__(self):
        """Return the ingredient name."""
        return self.name


class Equipment(models.Model):
    """Equipment contains the name, a spoonacauar_id(if exists) and a link to a picture."""
    name = models.CharField(max_length=100, default='Unnamed Equipment')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    picture = models.URLField(default='')

    def __str__(self):
        """Return the equipment name."""
        return self.name


class RecipeStep(models.Model):
    """A recipe's step containing each cooking step of the recipe."""
    number = models.IntegerField(default=1)
    description = models.TextField(default='No description provided')
    recipe = models.ForeignKey('Recipe', related_name='steps', on_delete=models.CASCADE)

    def __str__(self):
        """Return the string containing the step number and description."""
        return f'Step {self.number}: {self.description[:50]}'


class IngredientList(models.Model):
    """The relations representing which ingredient is used in which recipe."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=100)


class EquipmentList(models.Model):
    """The relations representing which equipment is used in which recipe."""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=100, default="piece")


class Recipe(models.Model):
    """The recipe class containing information about the recipe and methods."""
    name = models.CharField(max_length=200, default='Unnamed Recipe')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    estimated_time = models.FloatField(default=0)
    images = models.ImageField(upload_to='recipe_images/', blank=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """Return the name of the recipe."""
        return self.name

    def get_difficulty(self) -> str:
        """Return the difficulty of the recipe based on custom rules."""
        if self.estimated_time < 30:
            return 'Easy'
        elif self.estimated_time < 60:
            return 'Medium'
        else:
            return 'Hard'

    def get_ingredients(self) -> QuerySet[IngredientList]:
        """Return a queryset of IngredientList which contains the ingredients of the recipe."""
        return IngredientList.objects.filter(recipe=self)

    def get_equipments(self) -> QuerySet[EquipmentList]:
        """Return a queryset of EquipmentList which contains the equipment of the recipe."""
        return EquipmentList.objects.filter(recipe=self)

    def get_steps(self) -> QuerySet[RecipeStep]:
        """Return a queryset of steps in the recipe."""
        return RecipeStep.objects.filter(recipe=self)
