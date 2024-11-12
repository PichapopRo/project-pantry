"""Generate response from the AI about the recipe."""

from webpage.models import Recipe, Ingredient
from webpage.modules.gpt_handler import GPTHandler
from decouple import config
import json
import logging
from enum import Enum

logger = logging.getLogger("AI_Recipe")


class Tags(Enum):
    """The name of tag keys that should be in the output from the GPT."""
    NAME_TAG: str = "name"
    DESCRIPTION_TAG: str = "description"
    AMOUNT_TAG: str = "amount"
    UNIT_TAG: str = "unit"


class AIRecipeAdvisor:
    """
    Generates a response from GPT about the recipe.
    
    :param _recipe: The recipe that the AI will take as an input.
    :param _gpt: The GPT model handler.
    """

    def __init__(self, recipe: Recipe):
        """
        Initialize the class and fill out the information to put into the AI.
        
        :param recipe: The recipe that you want to generate response from.
        """
        self._recipe = recipe
        self._gpt = GPTHandler(config("ALTER_PROMT"), "gpt-4o-mini")
        name = "The recipe name:" + self._recipe.name
        description = "Description:" + self._recipe.description
        ingredients = ""
        for ingre in self._recipe.get_ingredients():
            ingredients += ingre.ingredient.name + " " + str(ingre.amount) + " " + ingre.unit + "\n"
        diets = "Diet restrictions:" + ",".join(self._recipe.diets.all())
        self._ingredient_information = name + '\n' +\
            description + '\n' + \
            ingredients + '\n' + \
            diets
    
    def check_output_structure(self, output: list[dict[str, str | int]]) -> bool:
        """
        Check weather the output from ChatGPT has the correct format (correct key names and number of keys).
        
        :param output: The list generated from the output from GPT.
        :return: True, if the output is valid. Else, if it's not.
        """
        try:
            for ingredient in output:
                if len(ingredient.keys()) != len(Tags):
                    return False
                for tag in Tags:
                    if tag.value not in ingredient.keys():
                        return False
        except AttributeError:
            return False

        return True

    def get_alternative_ingredients(self, ingredients: list[Ingredient], special_ins: str = "") -> list[dict[str, str | int]]:
        """
        Generate an alternative ingredients to the ingredients specified.

        Raises an Exception when there's an error with the GPT model.

        :param ingredients: A list of ingredients to be suggested as alternative ingredients.
        :param special_ins: Special instructions, e.g., I don't like chocolate.
        :return: Returns a list of dictionaries with `name` and `description` keys.
        """
        LIMIT = 5
        lacking_ingredients = "The ingredient I don't have:" + ",".join([ingredient.name for ingredient in ingredients])
        query = self._ingredient_information + "\n" + \
            lacking_ingredients + "\n" + \
            "The special instruction:" + special_ins

        for _ in range(LIMIT):
            try:
                string_alternative_ingredients = self._gpt.generate(query)
                processed_alternative_ingredients = json.loads(string_alternative_ingredients)
                # If there's an error, the following line will not be executed.
                if not self.check_output_structure(processed_alternative_ingredients):
                    continue
                return processed_alternative_ingredients
            except json.decoder.JSONDecodeError:
                continue
        raise Exception("Error with LLM. Please try again.")
