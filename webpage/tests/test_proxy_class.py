"""Tests for the Diet model."""
from django.test import TestCase
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.models import Ingredient
from webpage.modules.builder import NormalRecipeBuilder
from django.contrib.auth.models import User
from webpage.modules.filter_objects import FilterParam
from webpage.modules.recipe_facade import RecipeFacade

class GetDataProxyTest(TestCase):
    """Test the Diet model."""
    
    def setUp(self):
        """Create a test proxy before each test."""
        self.proxy = GetDataProxy(GetDataSpoonacular())
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')


    def filter_recipe_with_ingredient(self):
        """Filter the recipes using an ingredient"""
        _ingredient = Ingredient(name="Test Ingredient 1")
        _recipe = NormalRecipeBuilder("Test", self.user)
        _recipe.build_ingredient(_ingredient, 2, 'Kg')
        _recipe.build_recipe().save()
        param = FilterParam(offset=1, number=3)
        param.add_ingredient(_ingredient)
        _list = self.proxy.filter_recipe(param)
        facade = RecipeFacade()
        facade.set_recipe(_recipe)
        self.assertEqual(len(_list), 3)
        self.assertEqual(2,3)
        self.assertEqual(_list[0].name, facade.name)