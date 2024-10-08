from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Ingredient')
    spoonacular_id = models.IntegerField(unique=True, default=0)
    picture = models.URLField(default='')

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Equipment')
    spoonacular_id = models.IntegerField(unique=True, default=0)
    picture = models.URLField(default='')

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    number = models.IntegerField(default=1)
    description = models.TextField(default='No description provided')
    recipe = models.ForeignKey('Recipe', related_name='steps', on_delete=models.CASCADE)

    def __str__(self):
        return f'Step {self.number}: {self.description[:50]}'


class Recipe(models.Model):
    name = models.CharField(max_length=200, default='Unnamed Recipe')
    spoonacular_id = models.IntegerField(unique=True, null=True)
    cooking_steps = models.JSONField(default=dict)
    estimated_time = models.FloatField(default=0)
    images = models.ImageField(upload_to='recipe_images/', blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    equipment = models.JSONField(default=dict)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name