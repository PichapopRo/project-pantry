"""Tests for the Equipment model."""
from django.test import TestCase
from django.db import IntegrityError
from webpage.models import Equipment


class EquipmentModelTest(TestCase):
    """Test the Equipment model."""

    @classmethod
    def setUpTestData(cls):
        """Create a test diet before each test."""
        cls.equipment, _ = Equipment.objects.get_or_create(
            name="Oven",
            spoonacular_id=456,
            picture="http://example.com/oven.jpg"
        )

    def test_equipment_create(self):
        """Test if the equipment object is created correctly."""
        self.assertIsInstance(self.equipment, Equipment)
        self.assertEqual(self.equipment, Equipment.objects.get(
            id=self.equipment.id))
        self.assertEqual(self.equipment.name, "Oven")
        self.assertEqual(self.equipment.spoonacular_id, 456)
        self.assertEqual(self.equipment.picture, "http://example.com/oven.jpg")
        self.assertTrue(Equipment.objects.filter(
            name="Oven",
            spoonacular_id=456,
            picture="http://example.com/oven.jpg").exists())

    def test_equipment_str(self):
        """Test that the string representation of the equipment."""
        self.assertEqual(str(self.equipment), "Oven")

    def test_unique_equipment_spoonacular_id(self):
        """Test that spoonacular_id is unique."""
        with self.assertRaises(IntegrityError):
            Equipment.objects.create(
                name="Microwave",
                spoonacular_id=456)
