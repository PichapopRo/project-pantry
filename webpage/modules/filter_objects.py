from dataclasses import dataclass, field
from typing import List

@dataclass
class FilterParam:
    """A parameter class used to store the filter's parameters."""
    offset: int
    number: int
    includeIngredients: List[str]
    excludeIngredients: List[str]
    equipment: List[str]
    diet: List[str]
    maxReadyTime: int  # Ensure this is placed before any default arguments
    cuisine: str

    def add_ingredient(self, ingredient_name: str, include: bool = True):
        """
        Add the ingredient into the filter options.
        
        :param ingredient_name: The name of the ingredient.
        :param include: If set to true, the ingredient will be included.
        """
        if include:
            self.includeIngredients.append(ingredient_name)
        else:
            self.excludeIngredients.append(ingredient_name)

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
        _dict = {}
        for param in field(FilterParam):
            _dict[param.name] = getattr(self, param.name)
        return _dict