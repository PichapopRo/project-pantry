from django.test import TestCase
from django.contrib.auth.models import User
from webpage.models import Ingredient, Recipe, IngredientList

class IngredientListModelTest(TestCase):
    def setUp(self):
        """Create test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(name="Test Recipe", poster_id=self.user)
        self.ingredient = Ingredient.objects.create(name="Flour", spoonacular_id=1)
        self.ingredient_list = IngredientList.objects.create(
            ingredient=self.ingredient,
            recipe=self.recipe,
            amount=500,
            unit="grams"
        )

    def test_ingredientlist_creation(self):
        """Test if the IngredientList object is created correctly."""
        self.assertEqual(self.ingredient_list.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_list.recipe, self.recipe)
        self.assertEqual(self.ingredient_list.amount, 500)
        self.assertEqual(self.ingredient_list.unit, "grams")

    def test_ingredientlist_relationship(self):
        """Test the relationships between IngredientList, Recipe, and Ingredient."""
        self.assertEqual(self.ingredient_list.ingredient.name, "Flour")
        self.assertEqual(self.ingredient_list.recipe.name, "Test Recipe")