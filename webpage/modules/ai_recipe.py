from webpage.models import Recipe, Ingredient, IngredientList
from webpage.modules.gpt_handler import GPTHandler
from decouple import config
import json
import logging

logger = logging.getLogger("AI_Recipe")


class AIConsult:
    def __init__(self, recipe: Recipe):
        self._recipe = recipe
        self._gpt = GPTHandler(config("ALTER_PROMT"), "gpt-4o-mini")
        name = "The recipe name:" + self._recipe.name
        description = "Description:" + self._recipe.description
        ingredients = ""
        for ingre in self._recipe.get_ingredients():
            ingredients += ingre.ingredient.name + " " + str(ingre.amount) + " " + ingre.unit + "\n"
        diets = "Diet restrictions:"
        for diet in self._recipe.diets.all():
            diets += diet.name + ","
        self._ingredient_information = name + '\n' +\
            description + '\n' + \
            ingredients + '\n' + \
            diets
            
    
    def get_alternative_recipes(self, ingredients: list[Ingredient], special_ins: str = "") -> list[dict[str, str | int]]:
        LIMIT = 5
        count = 0
        data: list[dict[str, str | int]]
        no_ingre = "The ingredient I don't have:"
        for ingredient in ingredients:
            no_ingre += ingredient.name + ","
        query = self._ingredient_information + "\n" + \
            no_ingre + "\n" + \
            "The special instruction:" + special_ins

        while True:
            if count >= LIMIT:
                raise Exception("Error with LLM. Please try again.")
            try:
                data = json.loads(self._gpt.generate(query))
                # If there's an error, the following line will not be executed.
                break
            except json.decoder.JSONDecodeError:
                count += 1
        return data
