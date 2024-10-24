from dataclasses import dataclass
from webpage.models import Recipe, Ingredient, Equipment, Diet, Step

@dataclass
class FilterObjects:
    diet: list[str|None] = []
    ingredients: list[str|None] = None
    offset: int = 0
    number: int = 0
    
    
    