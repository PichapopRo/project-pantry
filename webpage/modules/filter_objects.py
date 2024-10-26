from dataclasses import dataclass
from webpage.models import Recipe, Ingredient, Equipment, Diet, Step
from enum import Enum    
    
@dataclass
class FilterParam:
    include: list[dict[str, str|float|int]]
    exclude: list[dict[str, str|float|int]]
    offset: int = 0
    number: int = 0

    def add_filter(self, filter_name: str, filter_value: int|float|str, include: bool = True):
        if include:
            self.include.append({filter_name: filter_value})
        else:
            self.exclude.append({filter_name: filter_value})
    
    
    