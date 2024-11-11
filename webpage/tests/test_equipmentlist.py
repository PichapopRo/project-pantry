"""Tests for the EquipmentList model."""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from webpage.models import Equipment, Recipe, EquipmentList


class EquipmentListModelTest(TestCase):
    """Test the EquipmentList model."""

    @classmethod
    def setUpTestData(cls):
        """Create test data before each test."""
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        cls.recipe = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=timezone.now(),
            description="This is a pasta."
        )
        cls.equipment = Equipment.objects.create(
            name="Pan",
            spoonacular_id=333,
            picture="http://example.com/pan.jpg"
        )
        cls.equipment_list = EquipmentList.objects.create(
            equipment=cls.equipment,
            recipe=cls.recipe,
            amount=1,
            unit="piece"
        )

    def test_equipment_list_create(self):
        """Test if the EquipmentList object is created correctly."""
        self.assertIsInstance(self.equipment_list, EquipmentList)
        self.assertEqual(self.equipment_list, EquipmentList.objects.get(
            id=self.equipment_list.id))
        self.assertEqual(self.equipment_list.equipment, self.equipment)
        self.assertEqual(self.equipment_list.recipe, self.recipe)
        self.assertEqual(self.equipment_list.amount, 1)
        self.assertEqual(self.equipment_list.unit, "piece")
        self.assertTrue(EquipmentList.objects.filter(
            equipment=self.equipment,
            recipe=self.recipe,
            amount=1,
            unit="piece").exists())
