from dataclasses import dataclass, field
from webpage.models import Recipe, Ingredient, Equipment, Diet, Step
from enum import Enum    
    
@dataclass
class FilterParam:
    """A parameter class uses to store the filter's parameter."""
    includeIngredients: list[str]
    excludeIngredients: list[str]
    equipment: list[str]
    diet: list[str]
    maxReadyTime: int
    cuisine: str
    offset: int = 0
    number: int = 0

    def add_ingredient(self, ingredient_name: str, include: bool = True):
        """
        Add the ingredient into the filter options.
        
        :param ingredient_name: The name of the ingredient name.
        :param include: If set to true, the it means that you want that ingredient included in.
        """
        if include:
            self.includeIngredients.append(ingredient_name)
        else:
            self.excludeIngredients.append(ingredient_name)
            
    def __get_string(self, _list: list[str]) -> str:
        return ','.join(_list)
            
    @property
    def equipment(self) -> str:
        return self.__get_string(self.equipment)
    
    @property
    def diet(self) -> str:
        return self.__get_string(self.diet)
    
    @property
    def cuisine(self) -> str:
        return self.__get_string(self.cuisine)
    
    def get_param(self) -> dict:
        _dict = {}
        for param in field(self):
            _dict.update(
                {
                    param.name,
                    getattr(self, param.name)
                }
            )
    
    
    