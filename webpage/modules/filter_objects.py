from dataclasses import dataclass
from webpage.models import Recipe, Ingredient, Equipment, Diet, Step

@dataclass
class FilterObjects:
    name: str|None = None
    diet: list[str|None] = []
    ingredients: list[str|None] = None
    
    