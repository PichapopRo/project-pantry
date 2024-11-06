from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import Favourite, Recipe


class FavouriteModelTest(TestCase):
    """Test suite for the Favourite model."""

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
            poster_id=cls.user2,
            created_at=cls.time,
            description=cls.description,
            status="Pending"
        )
        cls.recipe2 = Recipe.objects.create(name="Soup",
                                            spoonacular_id=124,
                                            estimated_time=15,
                                            poster_id=cls.user2)
        cls.favourite = Favourite.objects.create(
            recipe=cls.recipe,
            user=cls.user,
        )
        cls.favourite2 = Favourite.objects.create(
            recipe=cls.recipe2,
            user=cls.user,
        )

    def test_favourite_create(self):
        """Test if the favourite object is created correctly."""
        self.assertIsInstance(self.favourite, Favourite)
        self.assertEqual(self.favourite,
                         Favourite.objects.get(id=self.favourite.id))
        self.assertEqual(self.favourite.recipe, self.recipe)
        self.assertEqual(self.favourite.user, self.user)
        self.assertTrue(Favourite.objects.filter(
            recipe=self.recipe,
            user=self.user, ).exists())

    def test_get_favourites(self):
        """Test the get_favourites method."""
        favourites = Favourite.get_favourites(self.user)
        self.assertEqual(favourites.count(), 2)
        self.assertIn(self.favourite, favourites)
        self.assertIn(self.favourite2, favourites)
        favourite = [favourite for favourite in favourites]
        self.assertListEqual(favourite, [self.favourite, self.favourite2])

    def test_nutritionList_str(self):
        """Test string representation of a Favourite."""
        self.assertEqual(str(self.favourite),
                         f"Favourite {self.recipe} by {self.user}")
