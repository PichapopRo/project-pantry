"""Tests for the Diet model."""
from django.test import TestCase
from django.db import IntegrityError
from webpage.models import Diet


class DietModelTest(TestCase):
    """Test the Diet model."""

    @classmethod
    def setUpTestData(cls):
        """Create a test diet before each test."""
        cls.diet = Diet.objects.create(name="Vegan")

    def test_diet_create(self):
        """Test if the diet object is created correctly."""
        self.assertIsInstance(self.diet, Diet)
        self.assertEqual(self.diet.name, "Vegan")
        self.assertTrue(Diet.objects.filter(name="Vegan").exists())

    def test_diet_str(self):
        """Test the string representation of the diet."""
        self.assertEqual(str(self.diet), "Vegan")

    def test_unique_diet_name(self):
        """Test if the diet name is unique."""
        with self.assertRaises(IntegrityError):
            Diet.objects.create(name="Vegan")
