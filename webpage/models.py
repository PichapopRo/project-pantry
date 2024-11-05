"""
This module defines the models for the recipe application, including models.

For Recipe, Ingredient, Equipment, Diet, Nutrition, and their relationships.
"""
from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    """An ingredient contains the name, a spoonacauar_id(if exists) and a link to a picture."""

    name = models.CharField(max_length=100, default='Unnamed Ingredient')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    picture = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Return the ingredient name."""
        return self.name


class Equipment(models.Model):
    """Equipment contains the name, a spoonacauar_id(if exists) and a link to a picture."""

    name = models.CharField(max_length=100, default='Unnamed Equipment')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    picture = models.CharField(max_length=200, null=True, blank=True)

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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100)


class EquipmentList(models.Model):
    """The relations representing which equipment is used in which recipe."""

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=100, default="piece")


class Diet(models.Model):
    """A diet contains a different kind of diet restriction such as vegan or vegetarian."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return the name of the diet."""
        return self.name


class Nutrition(models.Model):
    """Nutrition, contains a nutrition for each recipe."""

    name = models.CharField(max_length=100)
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)


class NutritionList(models.Model):
    """The relations representing which nutrition information is used in which recipe."""

    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        """Return the name of the nutrition."""
        return f'{self.nutrition.name}: {self.amount} {self.unit}'


class Recipe(models.Model):
    """The recipe class containing information about the recipe and methods."""

    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    name = models.CharField(max_length=200, default='Unnamed Recipe')
    spoonacular_id = models.IntegerField(unique=True, null=True, blank=True)
    estimated_time = models.FloatField(default=0)
    image = models.CharField(max_length=200, null=True, blank=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=300, null=True, blank=True)
    diets = models.ManyToManyField(Diet, related_name="recipes")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

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

    @property
    def favourites(self):
        """Return the favourites of the recipe."""
        return self.favourite_set.count()

    def get_ingredients(self) -> QuerySet[IngredientList]:
        """Return a queryset of IngredientList which contains the ingredients of the recipe."""
        return IngredientList.objects.filter(recipe=self)

    def get_equipments(self) -> QuerySet[EquipmentList]:
        """Return a queryset of EquipmentList which contains the equipment of the recipe."""
        return EquipmentList.objects.filter(recipe=self)

    def get_steps(self) -> QuerySet[RecipeStep]:
        """Return a queryset of steps in the recipe."""
        return RecipeStep.objects.filter(recipe=self)

    def get_nutrition(self) -> QuerySet[NutritionList]:
        """Return a queryset of NutritionList which contains the nutrition information for the recipe."""
        return NutritionList.objects.filter(recipe=self)


class Favourite(models.Model):
    """Favourites are used to store favourite recipes."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_favourites(cls, recipe: Recipe, user: User):
        """Return a queryset of Favourite recipes."""
        if not user or not user.is_authenticated:
            return None
        try:
            return cls.objects.filter(user=user).select_related('recipe')
        except Favourite.DoesNotExist:
            return None

    def __str__(self):
        """Return the name of the favourite."""
        return f'Favourite {self.recipe} by {self.user}'
