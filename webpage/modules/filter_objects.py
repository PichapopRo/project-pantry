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
    includeIngredients: List[str] = field(default_factory=list)
    equipment: List[str] = field(default_factory=list)
    diet: List[str] = field(default_factory=list)
    maxReadyTime: int = 9999
    cuisine: List[str] = field(default_factory=list)
    titleMatch: str = ""

    def add_ingredient(self, ingredient_name: str):
        """
        Add the ingredient into the filter options.
        
        :param ingredient_name: The name of the ingredient.
        """
        self.includeIngredients.append(ingredient_name)

    def __get_string(self, _list: List[str]) -> str:
        """
        Turn the list of parameters into a string format according to Spoonacular.
        
        :return: The string format according to Spoonacular.
        """
        return ','.join(_list)

    @property
    def ingredient_str(self) -> str:
        """"
        Get the string representation of ingredient for Spoonacular.
        
        :return: The string format according to Spoonacular.
        """
        return self.__get_string(self.includeIngredients)
        
    @property
    def equipment_str(self) -> str:
        """
        Get the string representation of equipment for Spoonacular.
        
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
            'includeIngredients': self.ingredient_str,
            'equipment': self.equipment_str,
            'diet': self.diet_str,
            'maxReadyTime': self.maxReadyTime,
            'titleMatch': self.titleMatch
        }

    def __repr__(self) -> str:
        return (f"FilterParam(offset={self.offset}, number={self.number}, "
                f"includeIngredients={self.includeIngredients}, equipment={self.equipment}, "
                f"diet={self.diet}, maxReadyTime={self.maxReadyTime}, "
                f"cuisine={self.cuisine})")