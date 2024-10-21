"""Test the NormalRecipeBuilder class and its methods."""
from django.contrib.auth.models import User
from django.test import TestCase
from webpage import models
from webpage.modules.builder import NormalRecipeBuilder


class TestNormalRecipeBuilderClass(TestCase):
    """Test the NormalRecipeBuilder class."""

    def test_build_step(self):
        """
        Test the build_step method on the NormalRecipeBuilder.

        The steps should be sorted by the number in ascending order.
        """
        # Create a test user
        test_user = User.objects.filter(username="for_test").first()
        if test_user is None:
            test_user = User.objects.create_user(
                username="for_test", password="Helloworld2123"
            )

        # Build the recipe
        builder = NormalRecipeBuilder(name="Bad stew", user=test_user)
        builder.build_step("do it")
        builder.build_step("do it again")
        builder.build_step("eat it")
        recipe = builder.build_recipe()
        steps = recipe.get_steps()

        # Check
        list_number = [1, 2, 3]
        descriptions = ["do it", "do it again", "eat it"]
        for index, step in enumerate(steps):
            self.assertEqual(step.number, list_number[index])
            self.assertEqual(step.description, descriptions[index])

        # Delete all created objects
        for step in steps:
            step.delete()
        recipe.delete()
        test_user.delete()

    def test_build_one_equipment(self):
        """
        Test the build_equipment method on the NormalRecipeBuilder.

        The Builder should be able to add equipment to the recipe.
        """
        # Create a test user
        test_user = User.objects.filter(username="for_test").first()
        if test_user is None:
            test_user = User.objects.create_user(
                username="for_test", password="Helloworld2123"
            )

        # Build the recipe
        builder = NormalRecipeBuilder(name="Bad stew", user=test_user)
        equipment = models.Equipment.objects.create(name="bad spoons")

        builder.build_equipment(equipment=equipment, amount=21, unit="Meters")
        recipe = builder.build_recipe()
        equipment_list = recipe.get_equipments().first()

        # Check
        self.assertEqual(equipment_list.amount, 21)
        self.assertEqual(equipment_list.unit, "Meters")
        self.assertEqual(equipment_list.equipment.name, "bad spoons")

        # Delete all created objects
        equipment.delete()
        recipe.delete()
        test_user.delete()

    def test_build_one_ingredient(self):
        """
        Test the build_ingredient method on the NormalRecipeBuilder.

        The Builder should be able to add ingredients to the recipe.
        """
        # Create a test user
        test_user = User.objects.filter(username="for_test").first()
        if test_user is None:
            test_user = User.objects.create_user(
                username="for_test", password="Helloworld2123"
            )

        # Build the recipe
        builder = NormalRecipeBuilder(name="Bad stew", user=test_user)
        ingredient = models.Ingredient.objects.create(name="bad banana")

        builder.build_ingredient(ingredient=ingredient, amount=64, unit="kg")
        recipe = builder.build_recipe()
        ingredient_list = recipe.get_ingredients().first()

        # Check
        self.assertEqual(ingredient_list.amount, 64)
        self.assertEqual(ingredient_list.unit, "kg")
        self.assertEqual(ingredient_list.ingredient.name, "bad banana")

        # Delete all created objects
        ingredient.delete()
        recipe.delete()
        test_user.delete()
