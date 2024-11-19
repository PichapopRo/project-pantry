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
        self._gpt = GPTHandler(config("ALTER_PROMT", default="default"), "gpt-4o-mini")
        self._difficulty_gpt = GPTHandler(config("DIFF_PROMPT", default="default"), "gpt-4o-mini")
        self._nutrition_gpt = GPTHandler(config("NUTRITION_PROMPT", default="default"), "gpt-4o-mini")
        name = "The recipe name:" + self._recipe.name
        description = "Description:" + self._recipe.description
        ingredients = ""
        for ingre in self._recipe.get_ingredients():
            ingredients += ingre.ingredient.name + " " + str(ingre.amount) + " " + ingre.unit + "\n"
        diets = "Diet restrictions:" + ",".join([diet.name for diet in self._recipe.diets.all()])
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

    def difficulty_calculator(self):
        """
        Calculate the difficulty of the recipe using the GPT model.

        :return: A string representing the difficulty level ("Easy", "Normal", "Hard").
        :raises: Exception if the GPT model fails to generate a valid difficulty response.
        """
        query = "Based on the following recipe, determine the difficulty level. " + \
                "The difficulty should be one of 'Easy', 'Normal', or 'Hard':\n\n" + \
                f"{self._ingredient_information}\n" + \
                "Steps:\n" + "\n".join([step.description for step in self._recipe.steps.all()])
        LIMIT = 5
        for _ in range(LIMIT):
            try:
                response = self._difficulty_gpt.generate(query)
                difficulty = response.strip()
                if difficulty in ["Easy", "Normal", "Hard"]:
                    return difficulty
            except Exception as e:
                logger.error(f"Error during difficulty calculation: {e}")
                continue
        raise Exception("Error with LLM in difficulty calculation. Please try again.")

    def nutrition_calculator(self):
        """
        Calculate the nutritional information of the recipe based on its ingredients.

        :return: A dictionary containing a list of nutrients, each with name, amount, unit, and percent of daily needs.
        :raises: Exception if the GPT model fails to generate valid nutritional information.
        """
        LIMIT = 5
        ingredients_query = ""
        for ingre in self._recipe.get_ingredients():
            ingredients_query += f"{ingre.ingredient.name}, amount: {ingre.amount} {ingre.unit}\n"

        query = ingredients_query

        for _ in range(LIMIT):
            try:
                response = self._nutrition_gpt.generate(query)
                nutrition_info = json.loads(response)
                if "nutrients" in nutrition_info and isinstance(
                        nutrition_info["nutrients"], list):
                    required_keys = {"name", "amount", "unit", "percentOfDailyNeeds"}
                    for nutrient in nutrition_info["nutrients"]:
                        if not required_keys.issubset(nutrient.keys()):
                            raise ValueError("Invalid structure for a nutrient entry.")
                    return nutrition_info
            except json.JSONDecodeError:
                logger.error("Error decoding JSON from GPT response.")
            except ValueError as e:
                logger.error(f"Validation error in response structure: {e}")
            except Exception as e:
                logger.error(f"Error during nutrition calculation: {e}")
                continue

        raise Exception("Error with LLM in nutrition calculation. Please try again.")
