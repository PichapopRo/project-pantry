"""Tests for the Favourite model."""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from webpage.models import Favourite, Recipe


class FavouriteModelTest(TestCase):
    """Test the Favourite model."""

    @classmethod
    def setUpTestData(cls):
        """Create initial data for all test methods."""
        cls.user1 = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            email='test@example2.com',
            password='testpassword2'
        )
        cls.recipe1 = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user2,
            created_at=timezone.now(),
            description="This is a pasta.",
            status="Pending"
        )
        cls.recipe2 = Recipe.objects.create(
            name="Soup",
            spoonacular_id=124,
            estimated_time=15,
            poster_id=cls.user2)
        cls.favourite = Favourite.objects.create(
            recipe=cls.recipe1,
            user=cls.user1,
        )
        cls.favourite2 = Favourite.objects.create(
            recipe=cls.recipe2,
            user=cls.user1,
        )

    def test_favourite_create(self):
        """Test if the favourite object is created correctly."""
        self.assertIsInstance(self.favourite, Favourite)
        self.assertEqual(self.favourite, Favourite.objects.get(
            id=self.favourite.id))
        self.assertEqual(self.favourite.recipe, self.recipe1)
        self.assertEqual(self.favourite.user, self.user1)
        self.assertTrue(Favourite.objects.filter(
            recipe=self.recipe1,
            user=self.user1, ).exists())

    def test_get_favourites_user(self):
        """Test the get_favourites method with authenticated user."""
        favourites = Favourite.get_favourites(self.user1)
        self.assertEqual(favourites.count(), 2)
        self.assertIn(self.favourite, favourites)
        self.assertIn(self.favourite2, favourites)
        favourite = [favourite for favourite in favourites]
        self.assertListEqual(favourite, [self.favourite, self.favourite2])

    def test_get_favourites_not_user(self):
        """Test the get_favourites method with unauthenticated or no user."""
        favourites = Favourite.get_favourites(None)
        self.assertIsNone(favourites)

    def test_nutritionList_str(self):
        """Test string representation of the favourite."""
        self.assertEqual(str(self.favourite),
                         f"Favourite {self.recipe1} by {self.user1}")
