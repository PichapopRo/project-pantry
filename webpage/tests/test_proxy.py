from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from webpage.models import Ingredient, IngredientList, Equipment, EquipmentList, Recipe, Diet
from webpage.modules.proxy import GetDataSpoonacular, GetDataProxy, GetData


class GetDataProxyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.mock_service = MagicMock(spec=GetData)
        cls.service = GetDataProxy(service=None, queryset=Recipe.objects.all())
        cls.time = timezone.now()
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.recipe1 = Recipe.objects.create(
            name="Steak",
            spoonacular_id=111,
            estimated_time=55,
            image="http://example.com/steak.jpg",
            poster_id=cls.user,
            created_at=cls.time,
            description="This is a steak."
        )
        cls.recipe2 = Recipe.objects.create(
            name="Pork Hamburger",
            spoonacular_id=222,
            estimated_time=45,
            image="http://example.com/porkhamburger.jpg",
            poster_id=cls.user,
            created_at=cls.time,
            description="This is a pork hamburger."
        )
        cls.recipe3 = Recipe.objects.create(
            name="Meat Hamburger",
            spoonacular_id=333,
            estimated_time=45,
            image="http://example.com/meathamburger.jpg",
            poster_id=cls.user,
            created_at=cls.time,
            description="This is a meat hamburger."
        )

    def test_find_by_spoonacular_id_existing(self):
        self.assertTrue(Recipe.objects.filter(spoonacular_id=222).exists())
        recipe = self.service.find_by_spoonacular_id(222)
        self.assertEqual(recipe.spoonacular_id, 222)
        self.assertEqual(recipe.name, "Pork Hamburger")

    @patch('requests.get')
    def test_find_by_spoonacular_id_non_existing(self, mock_get):
        pass

    def test_find_by_name_existing(self):
        self.assertTrue(Recipe.objects.filter(spoonacular_id=222).exists())
        self.assertTrue(Recipe.objects.filter(spoonacular_id=333).exists())
        recipes = self.service.find_by_name("Hamburger")
        self.assertEqual(recipes.count(), 2)
        self.assertEqual(recipes[0].name, "Pork Hamburger")
        self.assertEqual(recipes[0].spoonacular_id, 222)
        self.assertEqual(recipes[1].name, "Meat Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 333)

    @patch('requests.get')
    def test_find_by_name_non_existing(self, mock_get):
        pass

    def test_filter_by_diet(self):
        diet = Diet.objects.create(name="meat")
        self.recipe1.diets.add(diet)
        self.recipe2.diets.add(diet)
        recipes = self.service.filter_by_diet("meat")
        self.assertEqual(recipes.count(), 2)
        self.assertEqual(recipes[0].name, "Steak")
        self.assertEqual(recipes[0].spoonacular_id, 111)
        self.assertEqual(recipes[1].name, "Pork Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 222)

    def test_filter_by_ingredient(self):
        ingredient = Ingredient.objects.create(name="Bread")
        IngredientList.objects.create(
            ingredient=ingredient,
            recipe=self.recipe2,
            amount=200,
            unit="grams"
        )
        IngredientList.objects.create(
            ingredient=ingredient,
            recipe=self.recipe3,
            amount=200,
            unit="grams"
        )
        recipes = self.service.filter_by_ingredient("Bread")
        self.assertEqual(recipes.count(), 2)
        self.assertEqual(recipes[0].name, "Pork Hamburger")
        self.assertEqual(recipes[0].spoonacular_id, 222)
        self.assertEqual(recipes[1].name, "Meat Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 333)

    def test_filter_by_max_cooking_time(self):
        recipes = self.service.filter_by_max_cooking_time(50)
        self.assertEqual(recipes.count(), 2)
        self.assertEqual(recipes[0].name, "Pork Hamburger")
        self.assertEqual(recipes[0].spoonacular_id, 222)
        self.assertEqual(recipes[1].name, "Meat Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 333)

    def test_filter_by_equipment(self):
        equipment = Equipment.objects.create(name="Pan")
        EquipmentList.objects.create(
            equipment=equipment,
            recipe=self.recipe2,
            amount=1,
            unit="piece"
        )
        EquipmentList.objects.create(
            equipment=equipment,
            recipe=self.recipe3,
            amount=200,
            unit="piece"
        )
        recipes = self.service.filter_by_equipment("Pan")
        self.assertEqual(recipes.count(), 2)
        self.assertEqual(recipes[0].name, "Pork Hamburger")
        self.assertEqual(recipes[0].spoonacular_id, 222)
        self.assertEqual(recipes[1].name, "Meat Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 333)

    def test_filter_by_difficulty(self):
        recipes = self.service.filter_by_difficulty("Medium")
        self.assertEqual(recipes.count(), 3)
        self.assertEqual(recipes[0].name, "Steak")
        self.assertEqual(recipes[0].spoonacular_id, 111)
        self.assertEqual(recipes[1].name, "Pork Hamburger")
        self.assertEqual(recipes[1].spoonacular_id, 222)
        self.assertEqual(recipes[2].name, "Meat Hamburger")
        self.assertEqual(recipes[2].spoonacular_id, 333)


class GetDataSpoonacularTest(TestCase):
    """Test the GetDataSpoonacular class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.service = GetDataSpoonacular()
        cls.user, _ = User.objects.get_or_create(username="Spoonacular")

    @patch('requests.get')
    def test_find_by_spoonacular_id(self, mock_get):
        """Test the find_by_spoonacular_id method on the GetDataSpoonacular."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 123456,
            "title": "Mock Salad",
            "image": "http://example.com/salad.jpg",
            "readyInMinutes": 45,
            "summary": "This is a mock salad.",
            "extendedIngredients": [
                {"id": 1, "name": "Mock Apple", "image": "apple.jpg",
                 "measures": {"metric": {"amount": 2, "unitLong": "slice"}}}
            ],
            "equipment": [
                {"name": "Mock Fork", "image": "fork.jpg"},
                {"name": "Mock Bowl", "image": "bowl.jpg"}
            ],
            "diets": ["vegan", "keto"],
            "nutrients": [
                {"name": "Protein", "amount": 30, "unit": "grams"}
            ],
            "analyzedInstructions": [
                {"steps": [{"step": "Mock do it"},
                           {"step": "Mock do it again"},
                           {"step": "Mock eat it"}]}
            ]
        }
        recipe = self.service.find_by_spoonacular_id(123456)
        self.assertEqual(recipe.spoonacular_id, 123456)
        self.assertEqual(recipe.name, "Mock Salad")
        self.assertEqual(recipe.image, "http://example.com/salad.jpg")
        self.assertEqual(recipe.estimated_time, 45)
        self.assertEqual(recipe.description, "This is a mock salad.")
        self.assertEqual(recipe.poster_id, self.user)
        self.assertTrue(Recipe.objects.filter(spoonacular_id=123456).exists())

    @patch('requests.get')
    def test_find_by_name(self, mock_get):
        """Test the find_by_name method on the GetDataSpoonacular."""
        pass
