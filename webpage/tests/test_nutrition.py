from django.test import TestCase
from webpage.models import Nutrition

class NutritionModelTest(TestCase):
    def setUp(self):
        """Create a test nutrition item before each test."""
        self.nutrition = Nutrition.objects.create(name="Protein", spoonacular_id=12345)

    def test_nutrition_creation(self):
        """Test if the nutrition object is created correctly."""
        self.assertEqual(self.nutrition.name, "Protein")
        self.assertEqual(self.nutrition.spoonacular_id, 12345)
        self.assertIsInstance(self.nutrition, Nutrition)

    def test_unique_spoonacular_id(self):
        """Test if spoonacular_id is unique."""
        with self.assertRaises(Exception):
            Nutrition.objects.create(name="Carbs", spoonacular_id=12345)