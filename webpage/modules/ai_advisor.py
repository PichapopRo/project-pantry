"""Generate response from the AI about the recipe."""

from webpage.models import Recipe, Ingredient
from webpage.modules.gpt_handler import GPTHandler
from decouple import config
import json
import logging

logger = logging.getLogger("AI_Recipe")


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
        diets = "Diet restrictions:"
        for diet in self._recipe.diets.all():
            diets += diet.name + ","
        self._ingredient_information = name + '\n' +\
            description + '\n' + \
            ingredients + '\n' + \
            diets
            
        self.__NAME_TAG = "name"
        self.__DESCRIPTION_TAG = "description"
        self.__AMOUNT_TAG = "amount"
        self.__UNIT_TAG = "unit"
    
    def check_output_structure(self, output: list[dict[str, str | int]]) -> bool:
        """
        Check weather the output from ChatGPT has the correct format (correct key names and number of keys).
        
        :param output: The list generated from the output from GPT.
        :return: True, if the output is valid. Else, if it's not.
        """
        NUMBER_OF_ITEMS_IN_THE_DICTIONARY = 4
        try:
            for ingredient in output:
                if len(list(ingredient.keys())) != NUMBER_OF_ITEMS_IN_THE_DICTIONARY:
                    return False
                if self.__NAME_TAG not in ingredient.keys() \
                        or self.__DESCRIPTION_TAG not in ingredient.keys() \
                        or self.__AMOUNT_TAG not in ingredient.keys() \
                        or self.__UNIT_TAG not in ingredient.keys():
                    return False
        except AttributeError:
            return False

        return True

    def get_alternative_ingredients(self, ingredients: list[Ingredient], special_ins: str = "") -> list[dict[str, str | int]]:
        """
        Generate an alternative ingredients to the ingredients specified.
        
        Raises an Exeption when there's an error with the GPT model.
        
        :param ingredients: A list of ingrdients to be suggests an alternative ingredient.
        :param special_ins: Special instructions, eg. I don't like chocolate.
        :return: Returns a list of dictionary with ```name``` and ```description``` keys.
        """
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
                generated = self._gpt.generate(query)
                data = json.loads(generated)
                # If there's an error, the following line will not be executed.
                if not self.check_output_structure(data):
                    count += 1
                    continue
                break
            except json.decoder.JSONDecodeError:
                count += 1
        return data
