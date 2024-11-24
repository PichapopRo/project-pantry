"""Tests for the NutritionList model."""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import Nutrition, Recipe, NutritionList


class NutritionListModelTest(TestCase):
    """Test the NutritionList model."""

    @classmethod
    def setUpTestData(cls):
        """Create test data before each test."""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.recipe = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=timezone.now(),
            description="This is a pasta."
        )
        cls.nutrition = Nutrition.objects.create(
            name="Vitamin A",
            spoonacular_id=11,
        )
        cls.nutrition_list = NutritionList.objects.create(
            nutrition=cls.nutrition,
            recipe=cls.recipe,
            amount=200,
            unit="kcal"
        )

    def test_nutrition_list_create(self):
        """Test if the NutritionList object is created correctly."""
        self.assertIsInstance(self.nutrition_list, NutritionList)
        self.assertEqual(self.nutrition_list, NutritionList.objects.get(
            id=self.nutrition_list.id))
        self.assertEqual(self.nutrition_list.nutrition, self.nutrition)
        self.assertEqual(self.nutrition_list.recipe, self.recipe)
        self.assertEqual(self.nutrition_list.amount, 200)
        self.assertEqual(self.nutrition_list.unit, "kcal")
        self.assertTrue(NutritionList.objects.filter(
            nutrition=self.nutrition,
            recipe=self.recipe,
            amount=200,
            unit="kcal").exists())

    def test_nutritionList_str(self):
        """Test string representation of a NutritionList."""
        self.assertEqual(str(self.nutrition_list),
                         f"{self.nutrition_list.nutrition.name}: "
                         f"{self.nutrition_list.amount} {self.nutrition_list.unit}")
