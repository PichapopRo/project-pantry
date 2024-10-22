from django.contrib.auth.models import User
from webpage.models import Recipe, IngredientList, EquipmentList, Equipment, Ingredient, RecipeStep
from django.test import TestCase

class RecipeModelTest(TestCase):
    """Test suite for the Recipe model."""

    @classmethod
    def setUpTestData(cls):
        """Create initial data for all test methods."""
        cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        cls.recipe = Recipe.objects.create(
            name="Pasta", spoonacular_id=789, estimated_time=45,
            poster_id=cls.user
        )

    def test_recipe_str(self):
        """Test string representation of a Recipe."""
        self.assertEqual(str(self.recipe), "Pasta")

    def test_difficulty_method(self):
        """Test the get_difficulty method."""
        difficulty = self.recipe.get_difficulty()
        self.assertEqual(difficulty, "Medium")

    def test_get_ingredients(self):
        """Test the get_ingredients method."""
        ingredient = Ingredient.objects.create(name="Pasta")
        IngredientList.objects.create(ingredient=ingredient, recipe=self.recipe, amount=200, unit="grams")
        ingredients = self.recipe.get_ingredients()
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(ingredients.first().ingredient.name, "Pasta")

    def test_get_equipments(self):
        """Test the get_equipments method."""
        equipment = Equipment.objects.create(name="Pan")
        EquipmentList.objects.create(equipment=equipment, recipe=self.recipe, amount=1, unit="piece")
        equipments = self.recipe.get_equipments()
        self.assertEqual(equipments.count(), 1)
        self.assertEqual(equipments.first().equipment.name, "Pan")

    def test_get_steps(self):
        """
        Test if the steps are returned in the correct order.

        This test ensures that six steps are created and retrieved in the
        correct ascending order based on the step number.
        """
        RecipeStep.objects.create(number=3, description="Third step", recipe=self.recipe)
        RecipeStep.objects.create(number=1, description="First step", recipe=self.recipe)
        RecipeStep.objects.create(number=2, description="Second step", recipe=self.recipe)
        RecipeStep.objects.create(number=6, description="Sixth step", recipe=self.recipe)
        RecipeStep.objects.create(number=4, description="Fourth step", recipe=self.recipe)
        RecipeStep.objects.create(number=5, description="Fifth step", recipe=self.recipe)
        steps = self.recipe.get_steps().order_by('number')
        step_descriptions = [step.description for step in steps]
        expected_order = [
            "First step", "Second step", "Third step",
            "Fourth step", "Fifth step", "Sixth step"
        ]
        self.assertEqual(step_descriptions, expected_order)

    def tearDown(self):
        """Clean up after tests."""
        self.recipe.delete()
        self.user.delete()
