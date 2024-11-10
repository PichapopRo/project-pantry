from django.test import TestCase
from unittest.mock import patch, MagicMock
from webpage.models import Recipe, Ingredient, IngredientList
from webpage.modules.ai_recipe import AIConsult
from django.utils import timezone
from django.contrib.auth.models import User
import json

class AIConsultTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.time = timezone.now()
        cls.user, _ = User.objects.get_or_create(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Create mock ingredients
        cls.ingredient1 = Ingredient.objects.create(name="Flour")
        cls.ingredient2 = Ingredient.objects.create(name="Sugar")
        
        # Create a recipe with ingredients
        cls.recipe = Recipe.objects.create(
            name="Cake",
            description="A delicious cake",
            poster_id=cls.user,
            created_at=cls.time
        )
        IngredientList.objects.create(recipe=cls.recipe, ingredient=cls.ingredient1, amount="2", unit="cups")
        IngredientList.objects.create(recipe=cls.recipe, ingredient=cls.ingredient2, amount="1", unit="cup")

    @patch('webpage.modules.gpt_handler.GPTHandler.generate')
    def test_get_alternative_recipes_success(self, mock_generate):
        # Arrange
        mock_generate.return_value = '[{"name": "Alternative Cake 1", "description": "A healthier version of cake."},' + \
                                                '{"name": "Alternative Cake 2", "description": "A chocolate version of cake."}]'        

        ai_consult = AIConsult(self.recipe)

        # Act
        alternatives = ai_consult.get_alternative_recipes([self.ingredient1, self.ingredient2])

        # Assert
        self.assertEqual(len(alternatives), 2)
        self.assertEqual(alternatives[0]["name"], "Alternative Cake 1")
        self.assertEqual(alternatives[1]["name"], "Alternative Cake 2")

    @patch('webpage.modules.gpt_handler.GPTHandler.generate')
    def test_get_alternative_recipes_failure(self, mock_generate):
        # Arrange
        mock_generate.return_value = '{"name": "Alternative Cake 1", "descripti "A healthier version of cake."},' + \
                                                '{"name": "Alternative Cake 2", "description": "A chocolate version of cake."},'

        ai_consult = AIConsult(self.recipe)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ai_consult.get_alternative_recipes([self.ingredient1])
        