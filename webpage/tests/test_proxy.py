"""Tests for the GetDataProxy class and GetDataSpoonacular class."""
import re
from django.test import TestCase
import unittest
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from webpage.models import (Recipe, Ingredient, IngredientList,
                            Equipment, EquipmentList, Diet)
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from webpage.modules.recipe_facade import RecipeFacade
from decouple import config

API_KEY = config('API_KEY', default='fake-secret-key')


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
            name='Avocado Pork Salad',
            image='http://example.com/porksalad.jpg',
            estimated_time=30,
            description='This is a pork salad.',
            poster_id=cls.user
        )
        cls.recipe2 = Recipe.objects.create(
            spoonacular_id=2,
            name='Avocado Meat Salad',
            image='http://example.com/meatsalad.jpg',
            estimated_time=30,
            description='This is a meat salad.',
            poster_id=cls.user
        )
        cls.ingredient1 = Ingredient.objects.create(
            name="avocado",
            spoonacular_id=11,
            picture="http://example.com/avocado.jpg"
        )
        cls.ingredient2 = Ingredient.objects.create(
            name="carrot",
            spoonacular_id=22,
            picture="http://example.com/carrot.jpg"
        )
        IngredientList.objects.create(
            ingredient=cls.ingredient1,
            recipe=cls.recipe1,
            amount=2,
            unit="piece"
        )
        IngredientList.objects.create(
            ingredient=cls.ingredient1,
            recipe=cls.recipe2,
            amount=2,
            unit="piece"
        )
        IngredientList.objects.create(
            ingredient=cls.ingredient2,
            recipe=cls.recipe1,
            amount=2,
            unit="table"
        )
        IngredientList.objects.create(
            ingredient=cls.ingredient2,
            recipe=cls.recipe2,
            amount=2,
            unit="table"
        )
        cls.equipment1 = Equipment.objects.create(
            name="Pan",
            spoonacular_id=333,
            picture="http://pan.com/pan.jpg"
        )
        cls.equipment2 = Equipment.objects.create(
            name="bowl",
            spoonacular_id=444,
            picture="http://bowl.com/bowl.jpg"
        )
        EquipmentList.objects.create(
            equipment=cls.equipment1,
            recipe=cls.recipe1,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=cls.equipment1,
            recipe=cls.recipe2,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=cls.equipment2,
            recipe=cls.recipe1,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=cls.equipment2,
            recipe=cls.recipe2,
            amount=1,
            unit="piece"
        )
        cls.diet1 = Diet.objects.create(
            name="Vegan")
        cls.diet2 = Diet.objects.create(
            name="Gluten Free")
        cls.recipe1.diets.add(cls.diet1, cls.diet2)
        cls.recipe2.diets.add(cls.diet1, cls.diet2)

    def test_find_by_spoonacular_id_existing(self):
        """Test finding a recipe by spoonacular_id when it exists in the database."""
        recipe = self.get_data_proxy.find_by_spoonacular_id(
            self.recipe1.spoonacular_id)
        self.assertEqual(recipe, self.recipe1)

    def test_find_by_spoonacular_id_non_existing(self):
        """Test finding a recipe by spoonacular_id when it does not exist in the database."""
        if API_KEY != "github-api-testing":
            recipe = self.get_data_proxy.find_by_spoonacular_id(10)
            self.assertEqual(recipe.spoonacular_id, 10)

    def test_filter_recipe_includeIngredients1(self):
        facades = self.get_data_proxy.filter_recipe(
            FilterParam(
                offset=1,
                number=2,
                includeIngredients=[self.ingredient1.name,
                                    self.ingredient2.name]
            )
        )
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)


    def test_filter_recipe_includeIngredients2(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=3,
                    includeIngredients=[self.ingredient1.name,
                                        self.ingredient2.name]
                )
            )
            self.assertEqual(len(facades), 3)
            self.assertEqual(facades[0].get_recipe(), self.recipe1)
            self.assertEqual(facades[1].get_recipe(), self.recipe2)
            recipe_temp = facades[2].get_recipe()
            ingredient_list = [igl.ingredient.name for igl in
                               list(recipe_temp.get_ingredients())]
            self.assertTrue(any(re.search(r'\bavocados?\b',
                                          ingredient,
                                          re.IGNORECASE)
                                for ingredient in ingredient_list))
            self.assertTrue(any(re.search(r'\bcarrots?\b',
                                          ingredient,
                                          re.IGNORECASE)
                            for ingredient in ingredient_list))

    def test_filter_recipe_includeIngredients3(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=3,
                    number=2,
                    includeIngredients=[self.ingredient1.name,
                                        self.ingredient2.name]
                )
            )
            self.assertEqual(len(facades), 2)
            recipe_temp1 = facades[0].get_recipe()
            ingredient_list1 = [igl.ingredient.name for igl in
                                list(recipe_temp1.get_ingredients())]
            recipe_temp2 = facades[1].get_recipe()
            ingredient_list2 = [igl.ingredient.name for igl in
                                list(recipe_temp2.get_ingredients())]
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.ingredient1.name)}s?\b", ingredient,
                re.IGNORECASE) for ingredient in ingredient_list1))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.ingredient2.name)}s?\b", ingredient,
                re.IGNORECASE) for ingredient in ingredient_list1))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.ingredient1.name)}s?\b", ingredient,
                re.IGNORECASE) for ingredient in ingredient_list2))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.ingredient2.name)}s?\b", ingredient,
                re.IGNORECASE) for ingredient in ingredient_list2))

    def test_filter_recipe_diet1(self):
        facades = self.get_data_proxy.filter_recipe(
            FilterParam(
                offset=1,
                number=2,
                diet=[self.diet1.name,
                      self.diet2.name]
            )
        )
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)

    def test_filter_recipe_diet2(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=3,
                    diet=[self.diet1.name,
                          self.diet2.name]
                )
            )
            self.assertEqual(len(facades), 3)
            self.assertEqual(facades[0].get_recipe(), self.recipe1)
            self.assertEqual(facades[1].get_recipe(), self.recipe2)
            diets = [diet.name for diet in facades[2].get_recipe().diets.all()]
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet1.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet2.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets))

    def test_filter_recipe_diet3(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=3,
                    number=2,
                    diet=[self.diet1.name,
                          self.diet2.name]
                )
            )
            self.assertEqual(len(facades), 2)
            diets1 = [diet.name for diet in facades[0].get_recipe().diets.all()]
            diets2 = [diet.name for diet in facades[1].get_recipe().diets.all()]
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet1.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets1))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet2.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets1))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet1.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets2))
            self.assertTrue(any(re.search(
                rf"\b{re.escape(self.diet2.name)}s?\b", diet,
                re.IGNORECASE) for diet in diets2))

    def test_filter_recipe_maxReadyTime1(self):
        facades = self.get_data_proxy.filter_recipe(
            FilterParam(
                offset=1,
                number=2,
                maxReadyTime=40
            )
        )
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)

    def test_filter_recipe_maxReadyTime2(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=3,
                    maxReadyTime=40
                )
            )
            self.assertEqual(len(facades), 3)
            self.assertEqual(facades[0].get_recipe(), self.recipe1)
            self.assertEqual(facades[1].get_recipe(), self.recipe2)
            recipe_temp = facades[2].get_recipe()
            self.assertLessEqual(recipe_temp.estimated_time, 40)

    def test_filter_recipe_maxReadyTime3(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=3,
                    number=2,
                    maxReadyTime=40
                )
            )
            self.assertEqual(len(facades), 2)
            self.assertLessEqual(facades[0].get_recipe().estimated_time, 40)
            self.assertLessEqual(facades[1].get_recipe().estimated_time, 40)

    def test_filter_recipe_titleMatch1(self):
        """Test filtering recipes."""
        facades = self.get_data_proxy.filter_recipe(
            FilterParam(
                offset=1,
                number=2,
                titleMatch="salad"
            )
        )
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)

    def test_filter_recipe_titleMatch2(self):
        """Test filtering recipes."""
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=3,
                    titleMatch="salad"
                )
            )
            self.assertEqual(len(facades), 3)
            self.assertEqual(facades[0].get_recipe(), self.recipe1)
            self.assertEqual(facades[1].get_recipe(), self.recipe2)
            self.assertTrue(re.search(r'\bsalads?\b',
                                      facades[2].get_recipe().name,
                                      re.IGNORECASE))

    def test_filter_recipe_titleMatch3(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=3,
                    number=2,
                    titleMatch="salad"
                )
            )
            self.assertEqual(len(facades), 2)
            self.assertTrue(re.search(r'\bsalads?\b',
                                      facades[0].get_recipe().name,
                                      re.IGNORECASE))
            self.assertTrue(re.search(r'\bsalads?\b',
                                      facades[1].get_recipe().name,
                                      re.IGNORECASE))

    @unittest.skip("Skipping test_filter_recipe_titleMatch4")
    def test_filter_recipe_titleMatch4(self):
        if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=2,
                    titleMatch="fish"
                )
            )
            # facades[0].get_recipe().name = Greek-Style Baked Fish:
            # Fresh, Simple, and Delicious
            # facades[1].get_recipe().name = Winter Kimchi which is wrong
            self.assertEqual(len(facades), 2)
            self.assertTrue(re.search(r'\bfishs?\b',
                                      facades[0].get_recipe().name,
                                      re.IGNORECASE))
            self.assertTrue(re.search(r'\bfishs?\b',
                                      facades[1].get_recipe().name,
                                      re.IGNORECASE))

    def test_filter_recipe_all1(self):
        """"""
        facades = self.get_data_proxy.filter_recipe(
            FilterParam(
                offset=1,
                number=2,
                includeIngredients=[self.ingredient1.name,
                                    self.ingredient2.name],
                diet=[self.diet1.name,
                      self.diet2.name],
                maxReadyTime=40,
                titleMatch="salad"
            )
        )
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].get_recipe(), self.recipe1)
        self.assertEqual(facades[1].get_recipe(), self.recipe2)

    def test_filter_recipe_all2(self):
        """if API_KEY != "github-api-testing":
            facades = self.get_data_proxy.filter_recipe(
                FilterParam(
                    offset=1,
                    number=3,
                    includeIngredients=[self.ingredient1.name],
                    equipment=[self.equipment1.name],
                    diet=[self.diet1.name],
                    maxReadyTime=200,
                    titleMatch="avocado"
                )
            )
            self.assertEqual(len(facades), 3)
            self.assertEqual(facades[0].get_recipe(), self.recipe1)
            self.assertEqual(facades[1].get_recipe(), self.recipe2)
            print(facades[2].get_recipe())"""

    def test_convert_parameter(self):
        parameter = self.get_data_proxy.convert_parameter(
            FilterParam(
                offset=1,
                number=2,
                includeIngredients=["avocado",
                                    "carrots"],
                diet=["Paleo",
                      "Low FODMAP"],
                maxReadyTime=40,
                titleMatch="fish"
            )
        )
        expected_parameter = [
            {"ingredientlist__ingredient__name__icontains": "avocado"},
            {"ingredientlist__ingredient__name__icontains": "carrots"},
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

    @patch('requests.get')
    @patch('webpage.modules.builder.NormalRecipeBuilder.build_difficulty')
    def test_find_by_spoonacular_id(self, mock_build_difficulty, mock_get):
        """Test find_by_spoonacular_id method."""
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {
            "id": 123450,
            "title": "fruit salad",
            "readyInMinutes": 30,
            "image": "https://fruitsalad.com/image.jpg",
            "summary": "This is a fruit salad.",
            "extendedIngredients": [
                {
                    "id": 101,
                    "name": "apple",
                    "image": "apple.jpg",
                    "measures": {"metric": {"amount": 100,
                                            "unitLong": "grams"}}
                },
                {
                    "id": 121,
                    "name": "banana",
                    "image": "banana.jpg",
                    "measures": {"metric": {"amount": 100,
                                            "unitLong": "grams"}}
                }
            ],
            "analyzedInstructions": [
                {
                    "steps": [
                        {
                            "step": "Step 1"
                        },
                        {
                            "step": "Step 2"
                        }
                    ]
                }
            ],
            "equipment": [
                {
                    "name": "bowl",
                    "image": "bowl.jpg"
                },
                {
                    "name": "fork",
                    "image": "fork.jpg"
                }
            ],
            "diets": [
                "vegetarian"
            ],
            "nutrients": [
                {
                    "name": "Calories",
                    "amount": 200,
                    "unit": "kcal"
                }
            ]
        }
        def mock_set_difficulty(*args, **kwargs):
            recipe = args[0]._SpoonacularRecipeBuilder__recipe
            recipe.difficulty = "Unknown"
            recipe.save()
        mock_build_difficulty.side_effect = mock_set_difficulty
        recipe = self.get_data_spoonacular.find_by_spoonacular_id(
            123450)
        self.assertTrue(Recipe.objects.filter(spoonacular_id=123450).exists())
        self.assertEqual(recipe.poster_id.username, "Spoonacular")
        self.assertEqual(recipe.name, "fruit salad")
        ingredient_list = [igl.ingredient.name for igl in
                           list(recipe.get_ingredients())]
        self.assertEqual(["apple", "banana"], ingredient_list)
        equipment_list = [eql.equipment.name for eql in
                          list(recipe.get_equipments())]
        self.assertEqual(["bowl", "fork"], equipment_list)
        nutrition_list = [ntl.nutrition.name for ntl in
                          list(recipe.get_nutrition())]
        self.assertEqual(["Calories"], nutrition_list)
        step_list = [step.description for step in
                     list(recipe.get_steps().order_by("number"))]
        self.assertEqual(["Step 1", "Step 2"], step_list)
        self.assertEqual(recipe.image, "https://fruitsalad.com/image.jpg")
        self.assertEqual(recipe.estimated_time, 30)
        self.assertEqual(recipe.description, "This is a fruit salad.")
        diet_list = recipe.diets.all()
        self.assertEqual(diet_list.count(), 1)
        self.assertEqual(diet_list.first().name, "Vegetarian")
        self.assertEqual(recipe.spoonacular_id, 123450)
        self.assertEqual(recipe.difficulty, "Unknown")
        self.assertIsInstance(recipe, Recipe)

    @patch('requests.get')
    def test_find_by_spoonacular_id_not_found(self, mock_get):
        """Test find_by_spoonacular_id method when the recipe is not found."""
        mock_get.return_value = Mock(status_code=404)
        with self.assertRaises(Exception):
            self.get_data_spoonacular.find_by_spoonacular_id(123450)

    @patch('requests.get')
    def test_filter_recipe_success(self, mock_get):
        """Test filtering recipes with a successful response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [
                {
                    "id": 112233,
                    "title": "Apple Pie",
                    "image": "https://applepie.com/image.jpg"
                },
                {
                    "id": 223344,
                    "title": "Fish Pie",
                    "image": "https://fishpie.com/image.jpg"
                }
            ]
        }
        recipes_facade = self.get_data_spoonacular.filter_recipe(
            FilterParam(
                offset=0,
                number=2,
                titleMatch="Pie"
            ))
        self.assertIsInstance(recipes_facade[0], RecipeFacade)
        self.assertIsInstance(recipes_facade[1], RecipeFacade)
        self.assertEqual(recipes_facade[0].name, "Apple Pie")
        self.assertEqual(recipes_facade[0].id, 112233)
        self.assertEqual(recipes_facade[0].image,
                         "https://applepie.com/image.jpg")
        self.assertEqual(recipes_facade[1].name, "Fish Pie")
        self.assertEqual(recipes_facade[1].id, 223344)
        self.assertEqual(recipes_facade[1].image,
                         "https://fishpie.com/image.jpg")

    @patch('requests.get')
    def test_filter_recipe_no_results(self, mock_get):
        """Test filtering recipes with no results."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": []
        }
        recipes_facade = self.get_data_spoonacular.filter_recipe(
            FilterParam(
                offset=0,
                number=2,
                titleMatch="Pie"
            ))
        self.assertEqual(len(recipes_facade), 0)

    @patch('requests.get')
    def test_filter_recipe_error_response(self, mock_get):
        """Test filtering recipes with an error response."""
        mock_get.return_value.status_code = 500
        with self.assertRaises(Exception) as context:
            self.get_data_spoonacular.filter_recipe(
                FilterParam(
                    offset=0,
                    number=2,
                    titleMatch="Pie"
                ))
        self.assertIn("Error code:", str(context.exception))

    def test_convert_parameter(self):
        parameter = self.get_data_spoonacular.convert_parameter(
            FilterParam(
                offset=0,
                number=2,
                includeIngredients=["Apple", "Banana"],
                diet=["Vegan"],
                maxReadyTime=70,
                titleMatch="Pie"
            )
        )
        expected_parameter = {
            'includeIngredients': "Apple,Banana",
            'diet': 'Vegan',
            'maxReadyTime': 70,
            'titleMatch': "Pie"
        }
        self.assertEqual(parameter, expected_parameter)
