from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import Nutrition, Recipe, NutritionList


class NutritionListModelTest(TestCase):
    """Test the NutritionList model."""

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
        self.assertEqual(self.nutrition_list,
                         NutritionList.objects.get(id=self.nutrition_list.id))
        self.assertEqual(self.nutrition_list.nutrition, self.nutrition)
        self.assertEqual(self.nutrition_list.recipe, self.recipe)
        self.assertEqual(self.nutrition_list.amount, 200)
        self.assertEqual(self.nutrition_list.unit, "kcal")
        self.assertTrue(NutritionList.objects.filter(
            nutrition=self.nutrition,
            recipe=self.recipe,
            amount=200,
            unit="kcal").exists())

    def test_nutrition_list_relationship(self):
        """Test the relationships between NutritionList, Recipe, and Nutrition."""
        self.assertEqual(self.nutrition_list.nutrition.name, self.nutrition.name)
        self.assertEqual(self.nutrition_list.recipe.name, self.recipe.name)

    def test_nutritionList_str(self):
        """Test string representation of a NutritionList."""
        self.assertEqual(str(self.nutrition_list), "Vitamin A: 200 kcal")
