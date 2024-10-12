from django.test import TestCase
from webpage.modules.builder import NormalRecipeBuilder
from django.contrib.auth.models import User
from webpage import models
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

class TestNormalRecipeBuilderClass(TestCase):
    """Test the NormalRecipeBuilder class."""
    
    def test_build_step(self):
        """
        Test the build_step method on the NormalRecipeBuilder.
        
        The step should be sort by the number in the ascending orders.
        """
        # Create a test user
        self.__test_user = User.objects.filter(username = "for_test").first()
        if(self.__test_user is None):
            self.__test_user = User(username = "for_test", password="Helloworld2123")
            self.__test_user.save()
            
        # Build the recipe
        n = NormalRecipeBuilder(name="Bad stew", user=self.__test_user)        
        n.build_step("do it")
        n.build_step("do it again")
        n.build_step("eat it")
        recipe = n.build_recipe()
        steps = recipe.get_steps()
        
        # Check
        lst = ["do it", "do it again", "eat it"]
        index = 0
        for step in steps:
            self.assertEqual(step.description, lst[index])
            index += 1
        
        # Delete all of the objects created
        for step in steps:
            step.delete()
        recipe.delete()
        self.__test_user.delete()
        
    def test_build_one_equipment(self):
        """
        Test the build_equipment method on the NormalRecipeBuilder.
        
        The Builder should be able to build the Equipment into the Recipe.
        """
        # Create a test user
        self.__test_user = User.objects.filter(username = "for_test").first()
        if(self.__test_user is None):
            self.__test_user = User(username = "for_test", password="Helloworld2123")
            self.__test_user.save()
            
        # Build the recipe
        n = NormalRecipeBuilder(name="Bad stew", user=self.__test_user)
        eq1 = models.Equipment.objects.create(name="bad spoons")
        eq1.save()
        
        
        n.build_equipment(equipment=eq1, amount=21, unit="Meters")
        recipe = n.build_recipe()
        equipment = recipe.get_equipments().first()
        
        # Check
        self.assertEqual(equipment.amount, 21)
        self.assertEqual(equipment.unit, "Meters")
        self.assertEqual(equipment.equipment.name, "bad spoons")
        
        # Delete all of the objects created
        eq1.delete()
        recipe.delete()
        self.__test_user.delete()
        
    def test_build_one_ingredient(self):
        """
        Test the build_ingredient method on the NormalRecipeBuilder.
        
        The Builder should be able to build the Ingredient into the Recipe.
        """
        # Create a test user
        self.__test_user = User.objects.filter(username = "for_test").first()
        if(self.__test_user is None):
            self.__test_user = User(username = "for_test", password="Helloworld2123")
            self.__test_user.save()
            
        # Build the recipe
        n = NormalRecipeBuilder(name="Bad stew", user=self.__test_user)
        ig1 = models.Ingredient.objects.create(name="bad banana")
        ig1.save()
        
        
        n.build_ingredient(ingredient=ig1, amount=64, unit="kg")
        recipe = n.build_recipe()
        ingredient = recipe.get_ingredients().first()
        
        # Check
        self.assertEqual(ingredient.amount, 64)
        self.assertEqual(ingredient.unit, "kg")
        self.assertEqual(ingredient.ingredient.name, "bad banana")
        
        # Delete all of the objects created
        ig1.delete()
        recipe.delete()
        self.__test_user.delete()
        