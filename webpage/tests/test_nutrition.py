"""Tests for the Nutrition model."""
from django.test import TestCase
from django.db import IntegrityError
from webpage.models import Nutrition


class NutritionModelTest(TestCase):
    """Test the Nutrition model."""

    @classmethod
    def setUpTestData(cls):
        """Create initial data for all test methods."""
        cls.nutrition = Nutrition.objects.create(
            name="Protein",
            spoonacular_id=12345)

    def test_nutrition_create(self):
        """Test if the nutrition object is created correctly."""
        self.assertIsInstance(self.nutrition, Nutrition)
        self.assertEqual(self.nutrition, Nutrition.objects.get(
            id=self.nutrition.id))
        self.assertEqual(self.nutrition.name, "Protein")
        self.assertEqual(self.nutrition.spoonacular_id, 12345)
        self.assertTrue(Nutrition.objects.filter(
            name="Protein",
            spoonacular_id=12345).exists())

    def test_unique_nutrition_spoonacular_id(self):
        """Test if spoonacular_id is unique."""
        with self.assertRaises(IntegrityError):
            Nutrition.objects.create(
                name="Carbs",
                spoonacular_id=12345)
