from django.test import TestCase
from django.db import IntegrityError
from webpage.models import Ingredient


class IngredientModelTest(TestCase):
    """Test suite for the Ingredient model."""

    @classmethod
    def setUpTestData(cls):
        """
        Create an ingredient instance to use in the tests.
        """
        cls.ingredient = Ingredient.objects.create(
            name="Tomato",
            spoonacular_id=123,
            picture="http://example.com/tomato.jpg"
        )

    def test_ingredient_create(self):
        """Test if the ingredient object is created correctly."""
        self.assertIsInstance(self.ingredient, Ingredient)
        self.assertEqual(self.ingredient, Ingredient.objects.get(id=self.ingredient.id))
        self.assertEqual(self.ingredient.name, "Tomato")
        self.assertEqual(self.ingredient.spoonacular_id, 123)
        self.assertEqual(self.ingredient.picture, "http://example.com/tomato.jpg")
        self.assertTrue(Ingredient.objects.filter(name="Tomato",
                                                  spoonacular_id=123,
                                                  picture="http://example.com/tomato.jpg").exists())

    def test_ingredient_str(self):
        """
        Test that the string representation of an Ingredient instance is the ingredient's name.
        """
        self.assertEqual(str(self.ingredient), "Tomato")

    def test_unique_ingredient_spoonacular_id(self):
        """Test that spoonacular_id is unique."""
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="Rice", spoonacular_id=123)
