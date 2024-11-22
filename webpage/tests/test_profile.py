"""Tests for the Profile model."""
from django.test import TestCase
from django.contrib.auth.models import User
from webpage.models import Profile


class ProfileModelTest(TestCase):
    """Test the Profile model."""

    @classmethod
    def setUpTestData(cls):
        """Create test data before each test."""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.profile = Profile.objects.create(
            user=cls.user,
            chef_badge=True
        )

    def test_profile_create(self):
        """Test if the profile object is created correctly."""
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile, Profile.objects.get(
            id=self.profile.id))
        self.assertEqual(self.profile.user, self.user)
        self.assertTrue(self.profile.chef_badge)
        self.assertTrue(Profile.objects.filter(
            user=self.user,
            chef_badge=True).exists())

    def test_profile_str(self):
        """Test string representation of the profile."""
        self.assertEqual(str(self.profile),
                         f"{self.user.username}'s Profile")
