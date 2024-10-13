from django.test import TestCase
from django.contrib.auth.models import User
from webpage.models import Ingredient, Equipment, Recipe, RecipeStep, IngredientList, EquipmentList


class IngredientModelTest(TestCase):
    """Test suite for the Ingredient model."""

    def setUp(self):
        """
        Create an ingredient instance to use in the tests.
        """
        self.ingredient = Ingredient.objects.create(
            name="Tomato", spoonacular_id=123,
            picture="http://example.com/tomato.jpg"
        )

    def test_ingredient_str(self):
        """
        Test that the string representation of an Ingredient instance is the ingredient's name.
        """
        self.assertEqual(str(self.ingredient), "Tomato")

    def test_ingredient_fields(self):
        """
        Test that the fields of an Ingredient instance are set correctly.
        """
        ingredient = Ingredient.objects.get(id=self.ingredient.id)
        self.assertEqual(ingredient.spoonacular_id, 123)
        self.assertEqual(ingredient.picture, "http://example.com/tomato.jpg")


class EquipmentModelTest(TestCase):
    """Test suite for the Equipment model."""

    def setUp(self):
        """
        Create an equipment instance to use in the tests.
        """
        self.equipment = Equipment.objects.create(
            name="Oven", spoonacular_id=456,
            picture="http://example.com/oven.jpg"
        )

    def test_equipment_str(self):
        """
        Test that the string representation of an Equipment instance is the equipment's name.
        """
        self.assertEqual(str(self.equipment), "Oven")

    def test_equipment_fields(self):
        """
        Test that the fields of an Equipment instance are set correctly.
        """
        equipment = Equipment.objects.get(id=self.equipment.id)
        self.assertEqual(equipment.spoonacular_id, 456)
        self.assertEqual(equipment.picture, "http://example.com/oven.jpg")


class RecipeModelTest(TestCase):
    """Test suite for the Recipe model."""

    def setUp(self):
        """
        Create a user and a recipe instance to use in the tests.
        """
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.recipe = Recipe.objects.create(
            name="Pasta", spoonacular_id=789, estimated_time=45,
            poster_id=self.user
        )

    def test_recipe_str(self):
        """
        Test that the string representation of a Recipe instance is the recipe's name.
        """
        self.assertEqual(str(self.recipe), "Pasta")

    def test_difficulty_method(self):
        """
        Test that the get_difficulty method returns the correct difficulty level based on estimated time.
        """
        difficulty = self.recipe.get_difficulty()
        self.assertEqual(difficulty, "Medium")

    def test_get_ingredients(self):
        """
        Test that the get_ingredients method returns a queryset of ingredients associated with the recipe.
        """
        ingredient = Ingredient.objects.create(name="Pasta")
        IngredientList.objects.create(ingredient=ingredient, recipe=self.recipe, amount=200, unit="grams")
        ingredients = self.recipe.get_ingredients()
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(ingredients.first().ingredient.name, "Pasta")

    def test_get_equipments(self):
        """
        Test that the get_equipments method returns a queryset of equipment associated with the recipe.
        """
        equipment = Equipment.objects.create(name="Pan")
        EquipmentList.objects.create(equipment=equipment, recipe=self.recipe, amount=1, unit="piece")
        equipments = self.recipe.get_equipments()
        self.assertEqual(equipments.count(), 1)
        self.assertEqual(equipments.first().equipment.name, "Pan")

    def test_get_steps(self):
        """
        Test that the get_steps method returns a queryset of steps associated with the recipe.
        """
        RecipeStep.objects.create(number=1, description="Boil water", recipe=self.recipe)
        steps = self.recipe.get_steps()
        self.assertEqual(steps.count(), 1)
        self.assertEqual(steps.first().description, "Boil water")


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
        