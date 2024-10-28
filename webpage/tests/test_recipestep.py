from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import RecipeStep, Recipe


class RecipeStepModelTest(TestCase):
    """Test suite for the RecipeStep model."""

    @classmethod
    def setUpTestData(cls):
        """Create test data before each test."""
        cls.time = timezone.now()
        cls.description = ("Pasta is a type of food typically made from "
                           "an unleavened dough of wheat flour mixed with "
                           "water or eggs, and formed into sheets or other "
                           "shapes, then cooked by boiling or baking.")
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
            created_at=cls.time,
            description=cls.description
        )
        cls.recipe_step = RecipeStep.objects.create(number=1,
                                                    description="First step",
                                                    recipe=cls.recipe)

    def test_recipe_step_create(self):
        """Test if the RecipeStep object is created correctly."""
        self.assertIsInstance(self.recipe_step, RecipeStep)
        self.assertEqual(self.recipe_step,
                         RecipeStep.objects.get(id=self.recipe_step.id))
        self.assertEqual(self.recipe_step.number, 1)
        self.assertEqual(self.recipe_step.description, "First step")
        self.assertEqual(self.recipe_step.recipe, self.recipe)
        self.assertTrue(RecipeStep.objects.filter(
            number=1,
            description="First step",
            recipe=self.recipe).exists())

    def test_recipe_step_relationship(self):
        """Test the relationships between RecipeStep and Recipe."""
        self.assertEqual(self.recipe_step.recipe.name, "Pasta")

    def test_recipe_step_str(self):
        """Test string representation of a RecipeStep."""
        self.assertEqual(str(self.recipe_step), "Step 1: First step")
