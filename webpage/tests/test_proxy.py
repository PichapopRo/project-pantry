"""Tests for the GetDataProxy class and GetDataSpoonacular class."""
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from webpage.models import (Recipe, Ingredient, IngredientList,
                            Equipment, EquipmentList, Diet,
                            Nutrition, NutritionList, RecipeStep)
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from django.utils import timezone
import re


class GetDataProxyTest(TestCase):
    """Test the GetDataProxy class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()
        IngredientList.objects.all().delete()
        Equipment.objects.all().delete()
        EquipmentList.objects.all().delete()
        Diet.objects.all().delete()
        cls.get_data_proxy = GetDataProxy(service=GetDataSpoonacular())
        cls.user = User.objects.create_user(
            username="Spoonacular")
        cls.recipe1 = Recipe.objects.create(
            spoonacular_id=1,
            name='Pork Salad',
            image='http://example.com/porksalad.jpg',
            estimated_time=30,
            description='This is a pork salad.',
            poster_id=cls.user
        )
        cls.recipe2 = Recipe.objects.create(
            spoonacular_id=2,
            name='Meat Salad',
            image='http://example.com/meatsalad.jpg',
            estimated_time=30,
            description='This is a meat salad.',
            poster_id=cls.user
        )
        cls.recipe3 = Recipe.objects.create(
            spoonacular_id=3,
            name='Meat Steak',
            image='http://example.com/meatsteak.jpg',
            estimated_time=50,
            description='This is a meat steak.',
            poster_id=cls.user
        )

    def test_find_by_spoonacular_id_existing(self):
        """Test finding a recipe by spoonacular_id when it exists in the database."""
        recipe = self.get_data_proxy.find_by_spoonacular_id(
            self.recipe1.spoonacular_id)
        self.assertEqual(recipe, self.recipe1)

    def test_find_by_spoonacular_id_non_existing(self):
        """Test finding a recipe by spoonacular_id when it does not exist in the database."""
        recipe = self.get_data_proxy.find_by_spoonacular_id(10)
        self.assertEqual(recipe.spoonacular_id, 10)

    def test_find_by_name_existing(self):
        """Test finding recipes by name when they exist in the database."""
        recipe = self.get_data_proxy.find_by_name("Salad")
        recipe_list = [re.get_recipe() for re in recipe]
        self.assertEqual([self.recipe1, self.recipe2], recipe_list)

    def test_find_by_name_non_existing(self):
        """Test finding recipes by name when they do not exist in the database."""
        recipe = self.get_data_proxy.find_by_name("lentil soup")
        recipe_list = [r.get_recipe().name for r in recipe]
        self.assertTrue(any(re.search(r'\blentil soup\b',
                                      recipe,
                                      re.IGNORECASE)
                            for recipe in recipe_list))

    def test_filter_recipe_includeIngredients(self):
        ingredient1 = Ingredient.objects.create(
            name="avocado",
            spoonacular_id=11,
            picture="http://example.com/avocado.jpg"
        )
        ingredient2 = Ingredient.objects.create(
            name="carrot",
            spoonacular_id=22,
            picture="http://example.com/carrot.jpg"
        )
        IngredientList.objects.create(
            ingredient=ingredient1,
            recipe=self.recipe1,
            amount=2,
            unit="piece"
        )
        IngredientList.objects.create(
            ingredient=ingredient1,
            recipe=self.recipe2,
            amount=2,
            unit="piece"
        )
        IngredientList.objects.create(
            ingredient=ingredient2,
            recipe=self.recipe1,
            amount=2,
            unit="table"
        )
        IngredientList.objects.create(
            ingredient=ingredient2,
            recipe=self.recipe2,
            amount=2,
            unit="table"
        )
        filter_param = FilterParam(
            offset=1,
            number=3,
            includeIngredients=[ingredient1.name, ingredient2.name]
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 3)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)
        recipe_temp = facades[2].get_recipe()
        ingredient_list = [igl.ingredient.name for igl in
                           list(recipe_temp.get_ingredients())]
        self.assertTrue(any(re.search(r'\bavocado\b',
                                      ingredient,
                                      re.IGNORECASE)
                            for ingredient in ingredient_list))
        self.assertTrue(any(re.search(r'\bcarrot\b',
                                      ingredient,
                                      re.IGNORECASE)
                            for ingredient in ingredient_list))

    def test_filer_recipe_equipment(self):
        equipment1 = Equipment.objects.create(
            name="Pan",
            spoonacular_id=333,
            picture="http://example.com/pan.jpg"
        )
        equipment2 = Equipment.objects.create(
            name="bowl",
            spoonacular_id=444,
            picture="http://example.com/spoon.jpg"
        )
        EquipmentList.objects.create(
            equipment=equipment1,
            recipe=self.recipe1,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=equipment1,
            recipe=self.recipe2,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=equipment2,
            recipe=self.recipe1,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=equipment2,
            recipe=self.recipe2,
            amount=1,
            unit="piece"
        )
        filter_param = FilterParam(
            offset=1,
            number=3,
            equipment=[equipment1.name, equipment2.name]
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 3)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)
        recipe_temp = facades[2].get_recipe()
        equipment_list = [eql.equipment.name for eql in
                          list(recipe_temp.get_equipments())]
        self.assertTrue(any(re.search(r'\bpan\b',
                                      equipment,
                                      re.IGNORECASE)
                            for equipment in equipment_list))
        # ['food processor', 'frying pan'] means there is no bowl.
        self.assertTrue(any(re.search(r'\bBowl\b',
                                      equipment,
                                      re.IGNORECASE)
                            for equipment in equipment_list))

    def test_filter_recipe_diet(self):
        diet1 = Diet.objects.create(
            name="Paleo")
        diet2 = Diet.objects.create(
            name="Low FODMAP")
        self.recipe1.diets.add(diet1, diet2)
        self.recipe2.diets.add(diet1, diet2)
        filter_param = FilterParam(
            offset=1,
            number=3,
            diet=[diet1.name, diet2.name]
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 3)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)
        recipe_temp = facades[2].get_recipe()
        # AssertionError: False is not true
        self.assertTrue(recipe_temp.diets.filter(name="Paleo").exists())
        # AssertionError: False is not true
        self.assertTrue(recipe_temp.diets.filter(name="Low FODMAP").exists())

    def test_filter_recipe_maxReadyTime(self):
        filter_param = FilterParam(
            offset=1,
            number=3,
            maxReadyTime=40
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 3)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)
        recipe_temp = facades[2].get_recipe()
        self.assertLessEqual(recipe_temp.estimated_time, 40)

    def test_filter_recipe_cuisine(self):
        pass

    def test_filter_recipe_enough_titleMatch(self):
        """Test filtering recipes."""
        filter_param = FilterParam(
            offset=1,
            number=2,
            titleMatch="salad"
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)

    def test_filter_recipe_not_enough_titleMatch(self):
        filter_param = FilterParam(
            offset=1,
            number=2,
            titleMatch="steak"
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        # AssertionError: 3 != 2
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe3)
        recipe_temp = facades[1].get_recipe()
        self.assertIn("steak", recipe_temp.name.lower())

    def test_filter_recipe_not_enough_titleMatch2(self):
        filter_param = FilterParam(
            offset=1,
            number=2,
            titleMatch="fish"
        )
        facades = self.get_data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 2)
        recipe_temp1 = facades[0].get_recipe()
        recipe_temp2 = facades[1].get_recipe()
        self.assertIn("fish", recipe_temp1.name.lower())
        # AssertionError: 'fish' not found in 'winter kimchi'
        self.assertIn("fish", recipe_temp2.name.lower())

    def test_convert_parameter(self):
        filter_param = FilterParam(
            offset=1,
            number=2,
            includeIngredients=["avocado", "carrots"],
            equipment=["slow cooker", "bowl"],
            diet=["Paleo", "Low FODMAP"],
            maxReadyTime=40,
            cuisine=["Asian", "Chinese"],
            titleMatch="fish"
        )
        parameter = self.get_data_proxy.convert_parameter(filter_param)
        expected_parameter = [
            {"ingredientlist__ingredient__name__icontains": "avocado"},
            {"ingredientlist__ingredient__name__icontains": "carrots"},
            {"equipmentlist__equipment__name__icontains": "slow cooker"},
            {"equipmentlist__equipment__name__icontains": "bowl"},
            {"diets__name__icontains": "Paleo"},
            {"diets__name__icontains": "Low FODMAP"},
            {"estimated_time__lte": 40},
            {"name__contains": "fish"}]
        self.assertEqual(parameter, expected_parameter)


class GetDataSpoonacularTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.get_data_spoonacular = GetDataSpoonacular()
        cls.user = User.objects.create_user(
            username="Spoonacular")
        cls.recipe = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=12345,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=timezone.now(),
            description="This is a pasta.",
            status="Pending"
        )
        ingredient = Ingredient.objects.create(
            name="Noodle",
            spoonacular_id=111,
            picture="http://example.com/noodle.jpg"
        )
        IngredientList.objects.create(
            ingredient=ingredient,
            recipe=cls.recipe,
            amount=200,
            unit="grams"
        )
        equipment = Equipment.objects.create(
            name="Pan",
            spoonacular_id=333,
            picture="http://example.com/pan.jpg"
        )
        EquipmentList.objects.create(
            equipment=equipment,
            recipe=cls.recipe,
            amount=1,
            unit="piece"
        )
        nutrition = Nutrition.objects.create(
            name="Vitamin A",
            spoonacular_id=11,
        )
        NutritionList.objects.create(
            nutrition=nutrition,
            recipe=cls.recipe,
            amount=200,
            unit="kcal"
        )
        RecipeStep.objects.create(
            number=1,
            description="First step",
            recipe=cls.recipe)
        diet = Diet.objects.create(
            name="Mediterranean")
        cls.recipe.diets.add(diet)

    @patch('webpage.modules.builder.SpoonacularRecipeBuilder.__call_api')
    @patch('webpage.modules.builder.SpoonacularRecipeBuilder')
    def test_find_by_spoonacular_id(self, MockSpoonacularRecipeBuilder,
                                    mock_call_api):
        mock_call_api.return_value = None
        mock_builder_instance = MockSpoonacularRecipeBuilder.return_value
        mock_builder_instance.build_name.return_value = mock_builder_instance
        mock_builder_instance.build_ingredient.return_value = mock_builder_instance
        mock_builder_instance.build_equipment.return_value = mock_builder_instance
        mock_builder_instance.build_nutrition.return_value = mock_builder_instance
        mock_builder_instance.build_step.return_value = mock_builder_instance
        mock_builder_instance.build_details.return_value = mock_builder_instance
        mock_builder_instance.build_diet.return_value = mock_builder_instance
        mock_builder_instance.build_spoonacular_id.return_value = mock_builder_instance
        mock_builder_instance.build_recipe.return_value = self.recipe

        # Act
        get_data_spoonacular = GetDataSpoonacular()
        returned_recipe = get_data_spoonacular.find_by_spoonacular_id(
            12345)

        # Assert
        # Verify that the builder was instantiated with correct parameters
        MockSpoonacularRecipeBuilder.assert_called_once_with(name="",
                                                             spoonacular_id=12345)

        # Verify that all build methods were called
        mock_builder_instance.build_name.assert_called_once()
        mock_builder_instance.build_ingredient.assert_called_once()
        mock_builder_instance.build_equipment.assert_called_once()
        mock_builder_instance.build_nutrition.assert_called_once()
        mock_builder_instance.build_step.assert_called_once()
        mock_builder_instance.build_details.assert_called_once()
        mock_builder_instance.build_diet.assert_called_once()
        mock_builder_instance.build_spoonacular_id.assert_called_once()
        mock_builder_instance.build_recipe.assert_called_once()

        # Verify that the returned recipe is the mock_recipe
        self.assertEqual(returned_recipe, self.recipe)

        # Verify that the recipe was saved to the database
        self.assertTrue(
            Recipe.objects.filter(spoonacular_id=12345).exists())
