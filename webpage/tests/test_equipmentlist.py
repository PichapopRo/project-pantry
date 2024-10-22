"""Tests for the EquipmentList model."""
from django.test import TestCase
from django.contrib.auth.models import User
from webpage.models import Equipment, Recipe, EquipmentList


class EquipmentListModelTest(TestCase):
    """Test the EquipmentList model."""

    def setUp(self):
        """Create test data before each test."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe", poster_id=self.user
        )
        self.equipment = Equipment.objects.create(
            name="Oven", spoonacular_id=1
        )
        self.equipment_list = EquipmentList.objects.create(
            equipment=self.equipment,
            recipe=self.recipe,
            amount=1,
            unit="piece"
        )

    def test_equipmentlist_creation(self):
        """Test if the EquipmentList object is created correctly."""
        self.assertEqual(self.equipment_list.equipment, self.equipment)
        self.assertEqual(self.equipment_list.recipe, self.recipe)
        self.assertEqual(self.equipment_list.amount, 1)
        self.assertEqual(self.equipment_list.unit, "piece")

    def test_equipmentlist_relationship(self):
        """
        Test the relationships between EquipmentList, Recipe, 
        and Equipment.
        """
        self.assertEqual(self.equipment_list.equipment.name, "Oven")
        self.assertEqual(self.equipment_list.recipe.name, "Test Recipe")
