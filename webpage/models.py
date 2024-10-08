from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    spoonacular_id = models.IntegerField(unique=True)  # Storing API id
    picture = models.URLField()  # URL to the ingredient picture

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    spoonacular_id = models.IntegerField(unique=True)  # Storing API id
    picture = models.URLField()  # URL to the equipment picture

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    number = models.IntegerField()  # Step number
    description = models.TextField()  # Step instructions
    recipe = models.ForeignKey('Recipe', related_name='steps',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'Step {self.number}: {self.description[:50]}'


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    spoonacular_id = models.IntegerField(unique=True)
    steps = models.ManyToManyField(RecipeStep, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    equipment = models.ManyToManyField(Equipment, related_name="recipes")
    poster = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes", null=True, blank=True)

    def __str__(self):
        return self.name
