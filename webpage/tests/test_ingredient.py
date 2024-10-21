from django.test import TestCase
from webpage.models import Ingredient

class IngredientModelTest(TestCase):
    """Test suite for the Ingredient model."""

    def setUp(self):
        """
        Create an ingredient instance to use in the tests.
        """
        self.ingredient = Ingredient.objects.create(
            name="Tomato", spoonacular_id=123,
            picture="http://example.com/tomato.jpg"
        )

    def test_ingredient_str(self):
        """
        Test that the string representation of an Ingredient instance is the ingredient's name.
        """
        self.assertEqual(str(self.ingredient), "Tomato")

    def test_ingredient_fields(self):
        """
        Test that the fields of an Ingredient instance are set correctly.
        """
        ingredient = Ingredient.objects.get(id=self.ingredient.id)
        self.assertEqual(ingredient.spoonacular_id, 123)
        self.assertEqual(ingredient.picture, "http://example.com/tomato.jpg")