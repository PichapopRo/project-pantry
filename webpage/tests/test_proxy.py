"""Tests for the GetDataProxy class and GetDataSpoonacular class."""
from django.test import TestCase
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from webpage.models import (Recipe, Ingredient, IngredientList,
                            Equipment, EquipmentList, Diet)
from webpage.modules.proxy import GetDataProxy, GetDataSpoonacular
from webpage.modules.filter_objects import FilterParam
from webpage.modules.recipe_facade import RecipeFacade
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
        print(ingredient_list)
        self.assertTrue(any(re.search(r'\bavocados?\b',
                                      ingredient,
                                      re.IGNORECASE)
                            for ingredient in ingredient_list))
        self.assertTrue(any(re.search(r'\bcarrots?\b',
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
            picture="http://example.com/bowl.jpg"
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
        self.assertTrue(any(re.search(r'\bpans?\b',
                                      equipment,
                                      re.IGNORECASE)
                            for equipment in equipment_list))
        # ['food processor', 'frying pan'] means there is no bowl.
        self.assertTrue(any(re.search(r'\bBowls?\b',
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

    @patch('requests.get')
    def test_find_by_spoonacular_id(self, mock_get):
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
        print(nutrition_list)
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
        self.assertIsInstance(recipe, Recipe)

    @patch('requests.get')
    def test_find_by_spoonacular_id_not_found(self, mock_get):
        """Test find_by_spoonacular_id method when the recipe is not found."""
        mock_get.return_value = Mock(status_code=404)
        with self.assertRaises(Exception):
            self.get_data_spoonacular.find_by_spoonacular_id(123450)

    @patch('requests.get')
    def test_find_by_name(self, mock_get):
        """Test retrieving a recipe by name."""
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
                    "image": "https://fishsteak.com/image.jpg"
                }
            ]
        }
        recipes_facade = self.get_data_spoonacular.find_by_name("Pie")
        self.assertIsInstance(recipes_facade[0], RecipeFacade)
        self.assertIsInstance(recipes_facade[1], RecipeFacade)
        self.assertEqual(recipes_facade[0].name, "Apple Pie")
        self.assertEqual(recipes_facade[0].id, 112233)
        self.assertEqual(recipes_facade[0].image,
                         "https://applepie.com/image.jpg")
        self.assertEqual(recipes_facade[1].name, "Fish Pie")
        self.assertEqual(recipes_facade[1].id, 223344)
        self.assertEqual(recipes_facade[1].image,
                         "https://fishsteak.com/image.jpg")

    @patch('requests.get')
    def test_find_by_name_no_results(self, mock_get):
        """Test retrieving a recipe by name when no results are found."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": []}
        recipes = self.get_data_spoonacular.find_by_name("-")
        self.assertEqual(len(recipes), 0)

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
                equipment=["Pan", "Spoon"],
                diet=["Vegan"],
                maxReadyTime=70,
                titleMatch="Pie"
            )
        )
        expected_parameter = {
            'includeIngredients': "Apple,Banana",
            'equipment': "Pan,Spoon",
            'diet': 'Vegan',
            'maxReadyTime': 70,
            'titleMatch': "Pie"
        }
        self.assertEqual(parameter, expected_parameter)
