"""This module provides an objects related to filtering."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class FilterParam:
    """A parameter class used to store the filter's parameters."""
    
    offset: int
    number: int
    includeIngredients: List[str] = field(default_factory=list)
    diet: List[str] = field(default_factory=list)
    maxReadyTime: int = 9999
    titleMatch: str = ""

    def add_ingredient(self, ingredient_name: str):
        """
        Add the ingredient into the filter options.
        
        :param ingredient_name: The name of the ingredient.
        """
        self.includeIngredients.append(ingredient_name)

    def get_param(self) -> dict:
        """
        Get the parameter for filtering.
        
        :return: The dictionary of parameter that will be used to filter.
        """
        return {
            'includeIngredients': self.includeIngredients,
            'diet': self.diet,
            'maxReadyTime': self.maxReadyTime,
            'titleMatch': self.titleMatch
        }

    def __repr__(self) -> str:
        """Return the representation string of the object."""
        return (f"FilterParam("
                f"offset={self.offset}, "
                f"number={self.number}, "
                f"includeIngredients={self.includeIngredients}, "
                f"diet={self.diet}, "
                f"maxReadyTime={self.maxReadyTime}, "
                f"titleMatch={self.titleMatch}"
                f")")
