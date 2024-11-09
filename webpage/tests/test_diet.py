"""Tests for the Diet model."""
from django.test import TestCase
from django.db import IntegrityError
from webpage.models import Diet


class DietModelTest(TestCase):
    """Test the Diet model."""

    @classmethod
    def setUpTestData(cls):
        """Create a test diet before each test."""
        cls.diet, _ = Diet.objects.get_or_create(
            name="Mediterranean")

    def test_diet_create(self):
        """Test if the diet object is created correctly."""
        self.assertIsInstance(self.diet, Diet)
        self.assertEqual(self.diet, Diet.objects.get(
            id=self.diet.id))
        self.assertEqual(self.diet.name, "Mediterranean")
        self.assertTrue(Diet.objects.filter(
            name="Mediterranean").exists())

    def test_diet_str(self):
        """Test the string representation of the diet."""
        self.assertEqual(str(self.diet), "Mediterranean")

    def test_unique_diet_name(self):
        """Test if the diet name is unique."""
        with self.assertRaises(IntegrityError):
            Diet.objects.create(
                name="Mediterranean")
