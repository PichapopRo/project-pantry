from dataclasses import dataclass, field
from typing import List
from enum import Enum

class FilterOptions(Enum):
    includeIngredients = 'ingredientlist__ingredient__name__icontains'
    equipment = 'equipmentlist__equipment__name__icontains'
    diet = 'diets__name__icontains'
    maxReadyTime = 'estimated_time__lte'


@dataclass
class FilterParam:
    """A parameter class used to store the filter's parameters."""
    offset: int
    number: int
    includeIngredients: List[str]
    equipment: List[str]
    diet: List[str]
    maxReadyTime: int  # Ensure this is placed before any default arguments
    cuisine: str

    def add_ingredient(self, ingredient_name: str):
        """
        Add the ingredient into the filter options.
        
        :param ingredient_name: The name of the ingredient.
        :param include: If set to true, the ingredient will be included.
        """
        self.includeIngredients.append(ingredient_name)

    def __get_string(self, _list: List[str]) -> str:
        """
        Turn the list of parameter into a string format according to Spoonacular.
        
        :return: The string format according to Spoonacular.
        """
        return ','.join(_list)

    @property
    def equipment_str(self) -> str:
        """
        Get the Spoonacular
        
        :return: The string format according to Spoonacular.
        """
        return self.__get_string(self.equipment)

    @property
    def diet_str(self) -> str:
        return self.__get_string(self.diet)

    @property
    def cuisine_str(self) -> str:
        return self.__get_string(self.cuisine)

    def get_param(self) -> dict:
        return {
            'includeIngredients': self.includeIngredients,
            'equipment': self.equipment_str,
            'diet': self.diet_str,
            'maxReadyTime': self.maxReadyTime
        }