"""Tests for the Diet model."""
from django.test import TestCase
from webpage.models import Diet


class DietModelTest(TestCase):
    """Test the Diet model."""

    def setUp(self):
        """Create a test diet before each test."""
        self.diet = Diet.objects.create(name="vegan")

    def test_diet_creation(self):
        """Test if the diet object is created correctly."""
        self.assertEqual(self.diet.name, "vegan")
        self.assertIsInstance(self.diet, Diet)

    def test_diet_str_method(self):
        """Test the string representation of the diet."""
        self.assertEqual(str(self.diet), "vegan")

    def test_unique_diet_name(self):
        """Test if the diet name is unique."""
        with self.assertRaises(Exception):
            Diet.objects.create(name="vegan")
