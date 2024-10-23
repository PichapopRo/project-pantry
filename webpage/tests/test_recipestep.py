from unittest import TestCase
from django.contrib.auth.models import User
from webpage.models import RecipeStep, Recipe
import pytest

@pytest.mark.django_db
class RecipeStepModelTest(TestCase):
    """Test suite for the RecipeStep model."""

    def setUp(self):
        """
        Create a user, a recipe, and a recipe step instance to use in the tests.
        """
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.recipe = Recipe.objects.create(
            name="Salad", poster_id=self.user
        )
        self.step = RecipeStep.objects.create(
            number=1, description="Chop vegetables", recipe=self.recipe
        )

    def test_recipe_step_str(self):
        """
        Test that the string representation of a RecipeStep instance includes the step number and a portion of the description.
        """
        expected_str = "Step 1: Chop vegetables"
        self.assertEqual(str(self.step), expected_str)
