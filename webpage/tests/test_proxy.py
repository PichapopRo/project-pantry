from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from webpage.models import Recipe
from webpage.modules.proxy import GetDataSpoonacular


class GetDataSpoonacularTest(TestCase):
    """Test the GetDataSpoonacular class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.service = GetDataSpoonacular()
        cls.user, _ = User.objects.get_or_create(username="Spoonacular")
        cls.mock_response = {
            "results": [
                {
                    "id": 123456,
                    "title": "Mock Salad",
                    "image": "http://example.com/salad.jpg",
                    "readyInMinutes": 45,
                    "summary": "This is a mock salad.",
                    "extendedIngredients": [
                        {"id": 1, "name": "Mock Apple", "image": "apple.jpg",
                         "measures": {
                             "metric": {"amount": 2, "unitLong": "slice"}}}
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
                },
                {
                    "id": 123,
                    "title": "Mock Stew",
                    "image": "http://example.com/stew.jpg",
                    "readyInMinutes": 70,
                    "summary": "This is a mock stew.",
                    "extendedIngredients": [
                        {"id": 1, "name": "Mock Pork", "image": "pork.jpg",
                         "measures": {
                             "metric": {"amount": 2, "unitLong": "slice"}}}
                    ],
                    "equipment": [
                        {"name": "Mock Fork", "image": "fork.jpg"},
                        {"name": "Mock Bowl", "image": "bowl.jpg"}
                    ],
                    "diets": ["keto"],
                    "nutrients": [
                        {"name": "Protein", "amount": 30, "unit": "grams"}
                    ],
                    "analyzedInstructions": [
                        {"steps": [{"step": "Mock do it"},
                                   {"step": "Mock do it again"},
                                   {"step": "Mock eat it"}]}
                    ]
                }
            ]
        }

    @patch('requests.get')
    def test_find_by_spoonacular_id(self, mock_get):
        """Test the find_by_spoonacular_id method on the GetDataSpoonacular."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = \
        self.mock_response["results"][0]
        recipe = self.service.find_by_spoonacular_id(123456)
        self.assertEqual(recipe.spoonacular_id, 123456)
        self.assertEqual(recipe.name, "Mock Salad")
        self.assertEqual(recipe.image, "http://example.com/salad.jpg")
        self.assertEqual(recipe.estimated_time, 45)
        self.assertEqual(recipe.description, "This is a mock salad.")
        self.assertEqual(recipe.poster_id, self.user)

    @patch('requests.get')
    def test_find_by_name(self, mock_get):
        """Test the find_by_name method on the GetDataSpoonacular."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response

        with patch.dict('os.environ', {'SPOONACULAR_API_KEY': MOCK_API_KEY}):
            recipes = self.service.find_by_name("Mock")

        self.assertEqual(len(recipes), 2)

        # Test first recipe
        recipe1 = recipes[0]
        self.assertEqual(recipe1.spoonacular_id, 123456)
        self.assertEqual(recipe1.name, "Mock Salad")
        self.assertEqual(recipe1.image, "http://example.com/salad.jpg")
        self.assertEqual(recipe1.estimated_time, 45)
        self.assertEqual(recipe1.description, "This is a mock salad.")

        # Test second recipe
        recipe2 = recipes[1]
        self.assertEqual(recipe2.spoonacular_id, 123)
        self.assertEqual(recipe2.name, "Mock Stew")
        self.assertEqual(recipe2.image, "http://example.com/stew.jpg")
        self.assertEqual(recipe2.estimated_time, 70)
        self.assertEqual(recipe2.description, "This is a mock stew.")
