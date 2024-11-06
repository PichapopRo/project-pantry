from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User
from webpage.models import (Recipe, IngredientList, EquipmentList,
                            Equipment, Ingredient, RecipeStep,
                            Diet, Nutrition, NutritionList, Favourite)


class RecipeModelTest(TestCase):
    """Test suite for the Recipe model."""

    @classmethod
    def setUpTestData(cls):
        """Create initial data for all test methods."""
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
        cls.user2 = User.objects.create_user(
            username='testuser2',
            email='test@example2.com',
            password='testpassword2'
        )
        cls.recipe = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=cls.time,
            description=cls.description,
            status="Pending"
        )
        Favourite.objects.create(
            recipe=cls.recipe,
            user=cls.user,
        )
        Favourite.objects.create(
            recipe=cls.recipe,
            user=cls.user2,
        )

    def test_recipe_create(self):
        """Test if the recipe object is created correctly."""
        self.assertIsInstance(self.recipe, Recipe)
        self.assertEqual(self.recipe, Recipe.objects.get(id=self.recipe.id))
        self.assertEqual(self.recipe.name, "Pasta")
        self.assertEqual(self.recipe.spoonacular_id, 123)
        self.assertEqual(self.recipe.estimated_time, 45)
        self.assertEqual(self.recipe.image, "http://example.com/pasta.jpg")
        self.assertEqual(self.recipe.poster_id, self.user)
        self.assertEqual(self.recipe.created_at, self.time)
        self.assertEqual(self.recipe.description, self.description)
        self.assertEqual(self.recipe.status, "Pending")
        self.assertTrue(Recipe.objects.filter(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=self.user,
            created_at=self.time,
            description=self.description,
            status="Pending").exists())

    def test_recipe_diets_create(self):
        """Test if the recipe diets are created correctly."""
        diet1 = Diet.objects.create(name="Dairy-Free")
        diet2 = Diet.objects.create(name="Low-Carb")
        self.recipe.diets.add(diet1, diet2)
        diets = self.recipe.diets.all()
        self.assertEqual(diets.count(), 2)
        self.assertIn(diet1, diets)
        self.assertIn(diet2, diets)
        diet_names = [diet.name for diet in diets]
        self.assertListEqual(diet_names, ["Dairy-Free", "Low-Carb"])

    def test_recipe_str(self):
        """Test string representation of a Recipe."""
        self.assertEqual(str(self.recipe), "Pasta")

    def test_unique_recipe_spoonacular_id(self):
        """Test that spoonacular_id is unique for recipes."""
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(name="Salad",
                                  spoonacular_id=123,
                                  poster_id=self.user)

    def test_difficulty_Easy(self):
        """Test the get_difficulty Easy."""
        self.recipe2 = Recipe.objects.create(name="Soup",
                                             spoonacular_id=124,
                                             estimated_time=15,
                                             poster_id=self.user)
        self.assertEqual(self.recipe2.get_difficulty(), "Easy")

    def test_difficulty_Medium(self):
        """Test the get_difficulty Medium."""
        self.assertEqual(self.recipe.get_difficulty(), "Medium")

    def test_difficulty_Hard(self):
        """Test the get_difficulty Hard."""
        self.recipe3 = Recipe.objects.create(name="Steak",
                                             spoonacular_id=125,
                                             estimated_time=75,
                                             poster_id=self.user)
        self.assertEqual(self.recipe3.get_difficulty(), "Hard")

    def test_favourites(self):
        """Test the favourites"""
        self.assertEqual(self.recipe.favourites, 2)

    def test_get_ingredients(self):
        """Test the get_ingredients method."""
        ingredient1 = Ingredient.objects.create(
            name="Noodle",
            spoonacular_id=111,
            picture="http://example.com/noodle.jpg"
        )
        ingredient2 = Ingredient.objects.create(
            name="Tomato",
            spoonacular_id=222,
            picture="http://example.com/tomato.jpg"
        )
        ingredient_list1 = IngredientList.objects.create(
            ingredient=ingredient1,
            recipe=self.recipe,
            amount=200,
            unit="grams"
        )
        ingredient_list2 = IngredientList.objects.create(
            ingredient=ingredient2,
            recipe=self.recipe,
            amount=3,
            unit="slice"
        )
        ingredient_list = list(self.recipe.get_ingredients())
        self.assertListEqual(ingredient_list,
                             [ingredient_list1, ingredient_list2])

    def test_get_equipments(self):
        """Test the get_equipments method."""
        equipment1 = Equipment.objects.create(
            name="Pan",
            spoonacular_id=333,
            picture="http://example.com/pan.jpg"
        )
        equipment2 = Equipment.objects.create(
            name="Spoon",
            spoonacular_id=444,
            picture="http://example.com/spoon.jpg"
        )
        equipment_list1 = EquipmentList.objects.create(
            equipment=equipment1,
            recipe=self.recipe,
            amount=1,
            unit="piece"
        )
        equipment_list2 = EquipmentList.objects.create(
            equipment=equipment2,
            recipe=self.recipe,
            amount=1,
            unit="piece"
        )
        equipment_list = list(self.recipe.get_equipments())
        self.assertListEqual(equipment_list,
                             [equipment_list1, equipment_list2])

    def test_get_steps(self):
        """Test if the steps are returned in the correct order."""
        step3 = RecipeStep.objects.create(number=3,
                                          description="Third step",
                                          recipe=self.recipe)
        step1 = RecipeStep.objects.create(number=1,
                                          description="First step",
                                          recipe=self.recipe)
        step2 = RecipeStep.objects.create(number=2,
                                          description="Second step",
                                          recipe=self.recipe)
        steps = list(self.recipe.get_steps().order_by("number"))
        self.assertListEqual(steps, [step1, step2, step3])

    def test_get_nutrition(self):
        """Test the get_nutrition method."""
        nutrition1 = Nutrition.objects.create(
            name="Vitamin A",
            spoonacular_id=11,
        )
        nutrition2 = Nutrition.objects.create(
            name="Vitamin B",
            spoonacular_id=22,
        )
        nutrition_list1 = NutritionList.objects.create(
            nutrition=nutrition1,
            recipe=self.recipe,
            amount=200,
            unit="kcal"
        )
        nutrition_list2 = NutritionList.objects.create(
            nutrition=nutrition2,
            recipe=self.recipe,
            amount=300,
            unit="kcal"
        )
        nutrition_list = list(self.recipe.get_nutrition())
        self.assertListEqual(nutrition_list,
                             [nutrition_list1, nutrition_list2])
