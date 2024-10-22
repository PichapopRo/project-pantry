from django.test import TestCase
from django.contrib.auth.models import User
from webpage.models import Nutrition, Recipe, NutritionList

class NutritionListModelTest(TestCase):
    def setUp(self):
        """Create test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(name="Test Recipe", poster_id=self.user)
        self.nutrition = Nutrition.objects.create(name="Calories", spoonacular_id=1)
        self.nutrition_list = NutritionList.objects.create(
            nutrition=self.nutrition,
            recipe=self.recipe,
            amount=200.5,
            unit="kcal"
        )

    def test_nutritionlist_creation(self):
        """Test if the NutritionList object is created correctly."""
        self.assertEqual(self.nutrition_list.nutrition, self.nutrition)
        self.assertEqual(self.nutrition_list.recipe, self.recipe)
        self.assertEqual(self.nutrition_list.amount, 200.5)
        self.assertEqual(self.nutrition_list.unit, "kcal")

    def test_nutritionlist_relationship(self):
        """Test the relationships between NutritionList, Recipe, and Nutrition."""
        self.assertEqual(self.nutrition_list.nutrition.name, "Calories")
        self.assertEqual(self.nutrition_list.recipe.name, "Test Recipe")