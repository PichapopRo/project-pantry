from django.db import models


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    difficulty = models.IntegerField(default=1)


class Ingredient(models.Model):
    question = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=200)
