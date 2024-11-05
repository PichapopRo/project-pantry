"""Tests for the Diet model."""
from django.test import TestCase
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.models import Ingredient, Recipe
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


    def test_filter_recipe_with_ingredient(self):
        """Test the filter the recipes using an ingredient"""
        _ingredient2 = Ingredient(name="Moldy Cheese")
        _ingredient2.save()
        _recipe2 = NormalRecipeBuilder("Stuffs", self.user)
        _recipe2.build_ingredient(_ingredient2, 2, 'kg')
        _recipe2.build_details(image="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=667&crop=1")
        _recipe2.build_recipe().save()
        _ingredient = Ingredient(name="Test Ingredient 1")
        _ingredient.save()
        _recipe = NormalRecipeBuilder("Test", self.user)
        _recipe.build_ingredient(_ingredient, 2, 'Kg')
        _recipe.build_details(image="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=667&crop=1")
        _recipe.build_recipe().save()
        param = FilterParam(offset=1, number=1)
        param.add_ingredient("test")
        _list = self.proxy.filter_recipe(param)
        facade = RecipeFacade()
        facade.set_recipe(_recipe.build_recipe())
        self.assertEqual(len(_list), 1)
        self.assertEqual(_list[0].name, facade.name)
        
    def test_filter_recipe_with_name(self):
        """Test the filter with recipe name"""
        _recipe2 = NormalRecipeBuilder("Stuffs", self.user)
        _recipe2.build_details(image="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=667&crop=1")
        _recipe2.build_recipe().save()
        _recipe = NormalRecipeBuilder("Test", self.user)
        _recipe.build_details(image="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=1000&h=667&crop=1")
        _recipe.build_recipe().save()
        param = FilterParam(offset=1, number=1)
        param.titleMatch = "est"
        _list = self.proxy.filter_recipe(param)
        facade = RecipeFacade()
        facade.set_recipe(_recipe.build_recipe())
        self.assertEqual(len(_list), 1)
        self.assertEqual(_list[0].name, facade.name)
        
            