from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import Ingredient, Recipe, IngredientList


class IngredientListModelTest(TestCase):
    """Test the IngredientList model."""

    @classmethod
    def setUpTestData(cls):
        """Create test data before each test."""
        cls.user, _ = User.objects.get_or_create(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.recipe, _ = Recipe.objects.get_or_create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=timezone.now(),
            description="This is a pasta."
        )
        cls.ingredient, _ = Ingredient.objects.get_or_create(
            name="Noodle",
            spoonacular_id=111,
            picture="http://example.com/noodle.jpg"
        )
        cls.ingredient_list, _ = IngredientList.objects.get_or_create(
            ingredient=cls.ingredient,
            recipe=cls.recipe,
            amount=200,
            unit="grams"
        )

    def test_ingredient_list_create(self):
        """Test if the IngredientList object is created correctly."""
        self.assertIsInstance(self.ingredient_list, IngredientList)
        self.assertEqual(self.ingredient_list, IngredientList.objects.get(
            id=self.ingredient_list.id))
        self.assertEqual(self.ingredient_list.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_list.recipe, self.recipe)
        self.assertEqual(self.ingredient_list.amount, 200)
        self.assertEqual(self.ingredient_list.unit, "grams")
        self.assertTrue(IngredientList.objects.filter(
            ingredient=self.ingredient,
            recipe=self.recipe,
            amount=200,
            unit="grams").exists())
