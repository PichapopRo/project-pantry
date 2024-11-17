"""Tests for the NormalRecipeBuilder class and SpoonacularRecipeBuilder class."""
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.test import TestCase
from webpage.models import Ingredient, Equipment, Nutrition, Diet
from webpage.modules.builder import NormalRecipeBuilder, \
    SpoonacularRecipeBuilder


class NormalRecipeBuilderTest(TestCase):
    """Test the NormalRecipeBuilder class."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user and related objects."""
        cls.user = User.objects.create_user(
            username="for_test2",
            password="Helloworld2123")
        cls.builder = NormalRecipeBuilder(
            name="Stew",
            user=cls.user)
        cls.recipe = cls.builder.build_recipe()

    def test_build_details(self):
        """Test the build_details method on the NormalRecipeBuilder."""
        details = {
            "estimated_time": 50,
            "description": "This is a stew."
        }
        self.builder.build_details(**details)
        self.assertEqual(self.recipe.estimated_time, details["estimated_time"])
        self.assertEqual(self.recipe.description, details["description"])

    def test_build_recipe(self):
        """Test the build_recipe method on the NormalRecipeBuilder."""
        self.assertEqual(self.recipe.name, "Stew")
        self.assertEqual(self.recipe.poster_id, self.user)

    def test_build_ingredient(self):
        """Test the build_ingredient method on the NormalRecipeBuilder."""
        ingredient = Ingredient.objects.create(
            name="Banana")
        self.builder.build_ingredient(
            ingredient=ingredient,
            amount=2,
            unit="slice")
        ingredient_list = self.recipe.get_ingredients().first()
        self.assertEqual(ingredient_list.recipe, self.builder.build_recipe())
        self.assertEqual(ingredient_list.ingredient, ingredient)
        self.assertEqual(ingredient_list.amount, 2)
        self.assertEqual(ingredient_list.unit, "slice")

    def test_build_one_equipment(self):
        """Test the build_equipment method on the NormalRecipeBuilder."""
        equipment = Equipment.objects.create(
            name="Spoon")
        self.builder.build_equipment(
            equipment=equipment,
            amount=1,
            unit="piece")
        equipment_list = self.recipe.get_equipments().first()
        self.assertEqual(equipment_list.recipe, self.builder.build_recipe())
        self.assertEqual(equipment_list.equipment, equipment)
        self.assertEqual(equipment_list.amount, 1)
        self.assertEqual(equipment_list.unit, "piece")

    def test_build_step(self):
        """Test the build_step method on the NormalRecipeBuilder."""
        self.builder.build_step("do it")
        self.builder.build_step("do it again")
        self.builder.build_step("eat it")
        steps = self.recipe.get_steps()
        list_number = [1, 2, 3]
        descriptions = ["do it", "do it again", "eat it"]
        for index, step in enumerate(steps):
            self.assertEqual(step.number, list_number[index])
            self.assertEqual(step.description, descriptions[index])

    def test_build_nutrition(self):
        """Test the build_nutrition method on the NormalRecipeBuilder."""
        nutrition = Nutrition.objects.create(
            name="Protein")
        self.builder.build_nutrition(
            nutrition=nutrition,
            amount=30,
            unit="grams")
        nutrition_list = self.recipe.get_nutrition().first()
        self.assertEqual(nutrition_list.recipe, self.builder.build_recipe())
        self.assertEqual(nutrition_list.nutrition, nutrition)
        self.assertEqual(nutrition_list.amount, 30)
        self.assertEqual(nutrition_list.unit, "grams")

    def test_build_user(self):
        """Test the build_user method on the NormalRecipeBuilder."""
        new_user = User.objects.create_user(
            username="new_user",
            password="password")
        self.builder.build_user(
            user=new_user)
        self.assertEqual(self.recipe.poster_id, new_user)
        self.user = new_user

    def test_build_diet(self):
        """Test the build_diet method on the NormalRecipeBuilder."""
        diet1 = Diet.objects.create(
            name="Keto")
        diet2 = Diet.objects.create(
            name="Carnivore")
        self.builder.build_diet(
            diet=diet1)
        self.builder.build_diet(
            diet=diet2)
        self.assertIn(diet1, self.recipe.diets.all())
        self.assertIn(diet2, self.recipe.diets.all())

    def test_build_spoonacular_id(self):
        """Test the build_spoonacular_id method on the NormalRecipeBuilder."""
        self.builder.build_spoonacular_id(123456)
        self.assertEqual(self.recipe.spoonacular_id, 123456)


class SpoonacularRecipeBuilderTest(TestCase):
    """Test the SpoonacularRecipeBuilder class."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user and related objects."""
        cls.builder = SpoonacularRecipeBuilder(
            name="Mock Salad",
            spoonacular_id="123456")
        cls.recipe = cls.builder.build_recipe()
        cls.user = User.objects.get(
            username="Spoonacular")

    def test_create_spoonacular_user_not_none(self):
        """Test the __create_spoonacular_user method on the SpoonacularRecipeBuilder when the user is not none."""
        created_user = self.builder._SpoonacularRecipeBuilder__create_spoonacular_user()
        self.assertEqual(self.user, created_user)

    def test_create_spoonacular_user_none(self):
        """Test the __create_spoonacular_user method when the user does not exist."""
        User.objects.filter(
            username="Spoonacular").delete()
        self.builder._SpoonacularRecipeBuilder__create_spoonacular_user()
        self.assertEqual(self.user.username, "Spoonacular")
        self.user = User.objects.get(
            username="Spoonacular")

    @patch('requests.get')
    def test_call_api_success(self, mock_get):
        """Test that __call_api fetches data correctly when the API call is successful."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "title": "Mocked Salad",
            "image": "salad.jpg",
            "readyInMinutes": 30,
            "summary": "This is a salad."
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.builder._SpoonacularRecipeBuilder__call_api()
        self.assertTrue(self.builder._SpoonacularRecipeBuilder__api_is_called)
        self.assertEqual(self.builder._SpoonacularRecipeBuilder__data["title"],
                         "Mocked Salad")
        self.assertEqual(self.builder._SpoonacularRecipeBuilder__data["image"],
                         "salad.jpg")
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__data["readyInMinutes"],
            30)
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__data["summary"],
            "This is a salad.")

    @patch('requests.get')
    def test_call_api_failure(self, mock_get):
        """Test that __call_api raises an exception when the API call fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            self.builder._SpoonacularRecipeBuilder__call_api()
        self.assertEqual(str(context.exception), "Cannot load the recipe")

    @patch('requests.get')
    def test_fetch_equipment_success(self, mock_get):
        """Test that __fetch_equipment fetches data correctly when the API call is successful."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "equipment": [
                {"name": "Blender"},
                {"name": "Chopping Board"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.builder._SpoonacularRecipeBuilder__fetch_equipment()
        self.assertTrue(
            self.builder._SpoonacularRecipeBuilder__api_equipment_is_fetch)
        self.assertEqual(len(
            self.builder._SpoonacularRecipeBuilder__equipment_data[
                "equipment"]), 2)
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__equipment_data[
                "equipment"][0]["name"], "Blender")
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__equipment_data[
                "equipment"][1]["name"], "Chopping Board")

    @patch('requests.get')
    def test_fetch_equipment_failure(self, mock_get):
        """Test that __fetch_equipment raises an exception when the API call fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            self.builder._SpoonacularRecipeBuilder__fetch_equipment()
        self.assertEqual(str(context.exception), "Cannot load the recipe")

    @patch('requests.get')
    def test_fetch_nutrition_success(self, mock_get):
        """Test that __fetch_nutrition fetches data correctly when the API call is successful."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "nutrition": [
                {"name": "VitaminA"},
                {"name": "VitaminB"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.builder._SpoonacularRecipeBuilder__fetch_nutrition()
        self.assertTrue(
            self.builder._SpoonacularRecipeBuilder__api_nutrition_is_fetch)
        self.assertEqual(len(
            self.builder._SpoonacularRecipeBuilder__nutrition_data[
                "nutrition"]), 2)
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__nutrition_data[
                "nutrition"][0]["name"], "VitaminA")
        self.assertEqual(
            self.builder._SpoonacularRecipeBuilder__nutrition_data[
                "nutrition"][1]["name"], "VitaminB")

    @patch('requests.get')
    def test_fetch_nutrition_failure(self, mock_get):
        """Test that __fetch_nutrition raises an exception when the API call fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            self.builder._SpoonacularRecipeBuilder__fetch_nutrition()
        self.assertEqual(str(context.exception), "Cannot load the recipe")

    def test_strip_html(self):
        """Test that __strip_html converts HTML to plain text correctly."""
        html_content = "<strong>This is a salad.</strong> <p>Enjoy your meal!</p>"
        expected_text = "This is a salad. Enjoy your meal!"
        plain_text = self.builder._SpoonacularRecipeBuilder__strip_html(
            html_content)
        self.assertEqual(plain_text, expected_text)

    def test_link_equipment_image(self):
        """Test that __link_equipment_image converts text equipment picture to an URL image correctly."""
        plain_text = "This is a plain text."
        expected_url_image = "https://img.spoonacular.com/equipment_500x500/This is a plain text."
        url_image = self.builder._SpoonacularRecipeBuilder__link_equipment_image(
            plain_text)
        self.assertEqual(url_image, expected_url_image)

    def test_link_ingredient_image(self):
        """Test that __link_ingredient_image converts text ingredient picture to an URL image correctly."""
        plain_text = "This is a plain text."
        expected_url_image = "https://img.spoonacular.com/ingredients_500x500/This is a plain text."
        url_image = self.builder._SpoonacularRecipeBuilder__link_ingredient_image(
            plain_text)
        self.assertEqual(url_image, expected_url_image)

    @patch('requests.get')
    def test_build_details(self, mock_get):
        """Test the build_details method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "image": "http://example.com/salad.jpg",
            "readyInMinutes": 45,
            "summary": "This is a salad."
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_details()
        self.assertEqual(self.recipe.image, mock_response["image"])
        self.assertEqual(self.recipe.estimated_time,
                         mock_response["readyInMinutes"])
        self.assertEqual(self.recipe.description, "This is a salad.")

    @patch('requests.get')
    def test_build_name(self, mock_get):
        """Test the build_name method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "title": "Mock Salad",
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_name()
        self.assertEqual(self.recipe.name, mock_response["title"])

    def test_build_recipe(self):
        """Test the build_recipe method on the SpoonacularRecipeBuilder."""
        self.assertEqual(self.recipe.name, "Mock Salad")
        self.assertEqual(self.recipe.poster_id, self.user)

    @patch('requests.get')
    def test_build_ingredient(self, mock_get):
        """Test the build_ingredient method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "extendedIngredients": [
                {"id": 1,
                 "name": "Mock Apple",
                 "image": "apple.jpg",
                 "measures": {"metric": {"amount": 2,
                                         "unitLong": "slice"}}}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_ingredient()
        ingredient_list = self.recipe.get_ingredients().first()
        self.assertEqual(ingredient_list.ingredient.name, "Mock Apple")
        self.assertEqual(ingredient_list.amount, 2)
        self.assertEqual(ingredient_list.unit, "slice")

    @patch('requests.get')
    def test_build_step_existing(self, mock_get):
        """Test the existing build_step method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "analyzedInstructions": [
                {"steps": [{"step": "Mock do it"},
                           {"step": "Mock do it again"},
                           {"step": "Mock eat it"}]}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_step()
        steps = self.recipe.get_steps()
        list_number = [1, 2, 3]
        descriptions = ["Mock do it", "Mock do it again", "Mock eat it"]
        for index, step in enumerate(steps):
            self.assertEqual(step.number, list_number[index])
            self.assertEqual(step.description, descriptions[index])

    @patch('requests.get')
    def test_build_equipment(self, mock_get):
        """Test the build_equipment method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "equipment": [
                {"name": "Mock Fork",
                 "image": "fork.jpg"},
                {"name": "Mock Bowl",
                 "image": "bowl.jpg"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_equipment()
        equipment_list = self.recipe.get_equipments().all()
        self.assertEqual(equipment_list[0].equipment.name,
                         "Mock Fork")
        self.assertEqual(equipment_list[0].equipment.picture,
                         self.builder.
                         _SpoonacularRecipeBuilder__link_equipment_image(
                             "fork.jpg"))
        self.assertEqual(equipment_list[1].equipment.name,
                         "Mock Bowl")
        self.assertEqual(equipment_list[1].equipment.picture,
                         self.builder.
                         _SpoonacularRecipeBuilder__link_equipment_image(
                             "bowl.jpg"))

    @patch('requests.get')
    def test_build_diet(self, mock_get):
        """Test the build_diet method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "diets": ["vegan",
                      "keto"]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_diet()
        self.assertIn(Diet.objects.get(
            name="Vegan"), self.recipe.diets.all())
        self.assertIn(Diet.objects.get(
            name="Keto"), self.recipe.diets.all())

    @patch('requests.get')
    def test_build_nutrition(self, mock_get):
        """Test the build_nutrition method on the SpoonacularRecipeBuilder."""
        mock_response = {
            "nutrients": [
                {"name": "Protein",
                 "amount": 30,
                 "unit": "grams"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_nutrition()
        nutrition_list = self.recipe.get_nutrition().first()
        self.assertEqual(nutrition_list.nutrition.name, "Protein")
        self.assertEqual(nutrition_list.amount, 30)
        self.assertEqual(nutrition_list.unit, "grams")

    @patch('requests.get')
    def test_build_spoonacular_id(self, mock_get):
        """Test the build_spoonacular_id method on the SpoonacularRecipeBuilder."""
        mock_response = {"id": 123456}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        self.builder.build_spoonacular_id()
        self.assertEqual(self.recipe.spoonacular_id, 123456)
