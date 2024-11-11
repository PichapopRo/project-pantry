"""Tests for the RecipeStep model."""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import RecipeStep, Recipe


class RecipeStepModelTest(TestCase):
    """Test the RecipeStep model."""

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
        cls.recipe_step, _ = RecipeStep.objects.get_or_create(
            number=1,
            description="First step",
            recipe=cls.recipe)

    def test_recipe_step_create(self):
        """Test if the RecipeStep object is created correctly."""
        self.assertIsInstance(self.recipe_step, RecipeStep)
        self.assertEqual(self.recipe_step, RecipeStep.objects.get(
            id=self.recipe_step.id))
        self.assertEqual(self.recipe_step.number, 1)
        self.assertEqual(self.recipe_step.description, "First step")
        self.assertEqual(self.recipe_step.recipe, self.recipe)
        self.assertTrue(RecipeStep.objects.filter(
            number=1,
            description="First step",
            recipe=self.recipe).exists())

    def test_recipe_step_str(self):
        """Test string representation of the recipeStep."""
        self.assertEqual(str(self.recipe_step),
                         f"Step {self.recipe_step.number}: "
                         f"{self.recipe_step.description[:50]}")
