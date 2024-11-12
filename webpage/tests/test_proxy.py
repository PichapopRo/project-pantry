"""Tests for the model and model."""
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from webpage.models import Recipe
from webpage.modules.proxy import GetDataProxy, GetData, GetDataSpoonacular
from webpage.modules.recipe_facade import RecipeFacade
from webpage.modules.filter_objects import FilterParam


class GetDataProxyTest(TestCase):
    """Test the GetDataProxy class."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.service = MagicMock(
            spec=GetData)
        cls.proxy = GetDataProxy(
            service=cls.service)
        cls.user = User.objects.create_user(
            username="Spoonacular")

    def test_find_by_spoonacular_id_existing(self):
        """Test finding a recipe by spoonacular_id when it exists in the database."""
        Recipe.objects.create(
            spoonacular_id=123456,
            name='Mock Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock salad.',
            poster_id=self.user
        )
        self.service.find_by_spoonacular_id.return_value = None
        found_recipe = self.proxy.find_by_spoonacular_id(123456)
        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.spoonacular_id, 123456)
        self.assertEqual(found_recipe.name, 'Mock Salad')

    @patch('webpage.modules.proxy.Recipe.objects.filter')
    def test_find_by_spoonacular_id_non_existing(self, mock_filter):
        """Test finding a recipe by spoonacular_id when it does not exist in the database."""
        mock_filter.return_value.exists.return_value = False
        mock_recipe = Recipe.objects.create(
            spoonacular_id=123456,
            name='Mock Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock salad.',
            poster_id=self.user
        )
        self.service.find_by_spoonacular_id.return_value = mock_recipe
        found_recipe = self.proxy.find_by_spoonacular_id(123456)
        self.assertIsNotNone(found_recipe)
        self.assertEqual(found_recipe.spoonacular_id, 123456)
        self.assertEqual(found_recipe.name, 'Mock Salad')

    @patch('webpage.modules.proxy.Recipe.objects.filter')
    def test_find_by_name_existing(self, mock_filter):
        """Test finding recipes by name when they exist in the database."""
        mock_qs = MagicMock(spec=Recipe.objects.all())
        mock_recipe1 = Recipe.objects.create(
            spoonacular_id=11,
            name='Mock Pork Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock pork salad.',
            poster_id=self.user
        )
        mock_recipe2 = Recipe.objects.create(
            spoonacular_id=22,
            name='Mock Meat Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock meat salad.',
            poster_id=self.user
        )
        mock_qs.__iter__.return_value = iter([mock_recipe1, mock_recipe2])
        mock_filter.return_value = mock_qs
        facades = self.proxy.find_by_name("Salad")
        self.assertEqual(len(facades), 2)
        self.assertIsInstance(facades[0], RecipeFacade)
        self.assertIsInstance(facades[1], RecipeFacade)
        self.assertEqual(facades[0].get_recipe(), mock_recipe1)
        self.assertEqual(facades[1].get_recipe(), mock_recipe2)

    @patch('webpage.modules.proxy.Recipe.objects.filter')
    def test_find_by_name_non_existing(self, mock_filter):
        """Test finding recipes by name when they do not exist in the database."""
        mock_filter.return_value.exists.return_value = False
        recipe1 = Recipe.objects.create(
            spoonacular_id=11,
            name='Mock Pork Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock pork salad.',
            poster_id=self.user)
        recipe2 = Recipe.objects.create(
            spoonacular_id=22,
            name='Mock Meat Salad',
            image='http://example.com/salad.jpg',
            estimated_time=45,
            description='This is a mock meat salad.',
            poster_id=self.user
        )
        facade1 = RecipeFacade()
        facade1.set_recipe(recipe1)
        facade2 = RecipeFacade()
        facade2.set_recipe(recipe2)
        mock_facades = [facade1, facade2]
        self.service.find_by_name.return_value = mock_facades
        facades = self.proxy.find_by_name("Salad")
        self.assertEqual(len(facades), 2)
        self.assertEqual(facades[0].id, 11)
        self.assertEqual(facades[0].name, 'Mock Pork Salad')
        self.assertEqual(facades[1].id, 22)
        self.assertEqual(facades[1].name, 'Mock Meat Salad')

    def test_filter_recipe(self):
        """Test filtering recipes."""
        recipe1 = Recipe.objects.create(
            spoonacular_id=153,
            name='Pork Salad',
            image='http://example.com/salad.jpg',
            estimated_time=1,
            description='This is a pork salad.',
            poster_id=self.user
        )
        recipe2 = Recipe.objects.create(
            spoonacular_id=1,
            name='Meat Salad',
            image='http://example.com/salad.jpg',
            estimated_time=100,
            description='This is a meat salad.',
            poster_id=self.user
        )
        recipe3 = Recipe.objects.create(
            spoonacular_id=220,
            name='Meat Steak',
            image='http://example.com/steak.jpg',
            estimated_time=5,
            description='This is a meat steak.',
            poster_id=self.user
        )
        filter_param = FilterParam(
            offset=1,
            number=100,
            maxReadyTime=0,
        )
        data_proxy = GetDataProxy(service=GetDataSpoonacular())
        facades = data_proxy.filter_recipe(filter_param)
        self.assertEqual(len(facades), 2)




