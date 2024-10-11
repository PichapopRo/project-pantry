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
        
        The step should be sort by the number in the ascending order.s
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
        