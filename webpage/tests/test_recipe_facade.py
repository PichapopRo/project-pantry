from django.test import TestCase
from webpage.models import Recipe, Favourite
from django.contrib.auth.models import User
from webpage.modules.recipe_facade import RecipeFacade


class RecipeFacadeTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test_password'
        )
        user2 = User.objects.create_user(
            username="Spoonacular")
        cls.recipe = Recipe.objects.create(
            spoonacular_id=132,
            name='Pork Salad',
            image='http://example.com/porksalad.jpg',
            estimated_time=30,
            description='This is a pork salad.',
            poster_id=user
        )
        cls.recipe2 = Recipe.objects.create(
            spoonacular_id=231,
            name='Mock Meat Salad',
            image='http://example.com/meatsalad.jpg',
            estimated_time=30,
            description='This is a meat salad.',
            poster_id=user2
        )
        Favourite.objects.create(
            recipe=cls.recipe,
            user=user
        )
        cls.name2 = 'Mock Meat Salad'
        cls.id2 = 231
        cls.image2 = 'http://example.com/meatsalad.jpg'
        cls.facade1 = RecipeFacade()
        cls.facade2 = RecipeFacade()
        cls.facade3 = RecipeFacade()

    def test_set_recipe(self):
        self.facade2.set_recipe(self.recipe)
        self.assertEqual(self.facade2.get_recipe(), self.recipe)
        self.assertEqual(self.facade2.name, self.recipe.name)
        self.assertEqual(self.facade2.id, self.recipe.spoonacular_id)
        self.assertEqual(self.facade2.image, self.recipe.image)
        self.assertEqual(self.facade2.favorite, self.recipe.favourites)

    def test_set_by_spoonacular(self):
        self.facade3.set_by_spoonacular(self.name2, self.id2, self.image2)
        self.assertEqual(self.facade3.name, self.name2)
        self.assertEqual(self.facade3.id, self.id2)
        self.assertEqual(self.facade3.image, self.image2)
        self.assertEqual(self.facade3.favorite, 0)

    def test_get_recipe_none(self):
        with self.assertRaises(Exception) as context:
            self.facade1.get_recipe()
        self.assertEqual(str(context.exception), "Please set something")

    def test_get_recipe_recipe(self):
        self.facade2.set_recipe(self.recipe)
        self.assertEqual(self.facade2.get_recipe(), self.recipe)

    def test_get_recipe_spoonacular(self):
        self.facade3.set_by_spoonacular(self.name2, self.id2, self.image2)
        self.assertEqual(self.facade3.get_recipe(), self.recipe2)

    def test_str(self):
        self.assertEqual(str(self.facade1),
                         f"Recipe name: {self.facade1.name}, "
                         f"Recipe ID: {self.facade1.id}")
        self.assertEqual(str(self.facade2),
                         f"Recipe name: {self.facade2.name}, "
                         f"Recipe ID: {self.facade2.id}")
        self.assertEqual(str(self.facade3),
                         f"Recipe name: {self.facade3.name}, "
                         f"Recipe ID: {self.facade3.id}")
