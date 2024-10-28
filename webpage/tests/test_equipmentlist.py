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
        cls.recipe = Recipe.objects.create(
            name="Pasta",
            spoonacular_id=123,
            estimated_time=45,
            image="http://example.com/pasta.jpg",
            poster_id=cls.user,
            created_at=cls.time,
            description=cls.description
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
        self.assertEqual(self.equipment_list, EquipmentList.objects.get(id=self.equipment_list.id))
        self.assertEqual(self.equipment_list.equipment, self.equipment)
        self.assertEqual(self.equipment_list.recipe, self.recipe)
        self.assertEqual(self.equipment_list.amount, 1)
        self.assertEqual(self.equipment_list.unit, "piece")
        self.assertTrue(EquipmentList.objects.filter(
            equipment=self.equipment,
            recipe=self.recipe,
            amount=1,
            unit="piece").exists())

    def test_equipment_list_relationship(self):
        """Test the relationships between EquipmentList, Recipe, and Equipment."""
        self.assertEqual(self.equipment_list.equipment.name, "Pan")
        self.assertEqual(self.equipment_list.recipe.name, "Pasta")
