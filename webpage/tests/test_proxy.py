from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from webpage.models import Recipe
from webpage.modules.builder import SpoonacularRecipeBuilder
from webpage.modules.proxy import GetDataSpoonacular


class GetDataSpoonacularTest(TestCase):
    """Test the GetDataSpoonacular class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.service = GetDataSpoonacular()
        cls.user, _ = User.objects.get_or_create(username="Spoonacular")
        cls.spoonacular_id = 123456
        cls.recipe_name = "Mock Salad"
        cls.mock_response = {
            "id": cls.spoonacular_id,
            "title": cls.recipe_name,
            "image": "http://example.com/salad.jpg",
            "readyInMinutes": 45,
            "summary": "This is a mock salad.",
            "extendedIngredients": [
                {"id": 1, "name": "Mock Apple", "image": "apple.jpg",
                 "measures": {"metric": {"amount": 2, "unitLong": "slice"}}}
            ],
            "equipment": [
                {"name": "Mock Fork", "image": "fork.jpg"},
                {"name": "Mock Bowl", "image": "bowl.jpg"}
            ],
            "diets": ["vegan", "keto"],
            "nutrients": [
                {"name": "Protein", "amount": 30, "unit": "grams"}
            ],
            "analyzedInstructions": [
                {"steps": [{"step": "Mock do it"},
                           {"step": "Mock do it again"},
                           {"step": "Mock eat it"}]}
            ]
        }

    @patch('requests.get')
    def test_find_by_spoonacular_id(self, mock_get):
        """Test the find_by_spoonacular_id method on the GetDataSpoonacular."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response
        recipe = self.service.find_by_spoonacular_id(self.spoonacular_id)
        self.assertIsInstance(recipe, Recipe)
        self.assertEqual(recipe.spoonacular_id, self.spoonacular_id)
        self.assertEqual(recipe.name, self.recipe_name)
        self.assertEqual(recipe.image, "http://example.com/salad.jpg")
        self.assertEqual(recipe.estimated_time, 45)
        self.assertEqual(recipe.description, "This is a mock salad.")
        self.assertEqual(recipe.poster_id, self.user)
