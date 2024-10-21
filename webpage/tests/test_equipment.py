from django.test import TestCase
from webpage.models import Equipment

class EquipmentModelTest(TestCase):
    """Test suite for the Equipment model."""

    def setUp(self):
        """
        Create an equipment instance to use in the tests.
        """
        self.equipment = Equipment.objects.create(
            name="Oven", spoonacular_id=456,
            picture="http://example.com/oven.jpg"
        )

    def test_equipment_str(self):
        """
        Test that the string representation of an Equipment instance is the equipment's name.
        """
        self.assertEqual(str(self.equipment), "Oven")

    def test_equipment_fields(self):
        """
        Test that the fields of an Equipment instance are set correctly.
        """
        equipment = Equipment.objects.get(id=self.equipment.id)
        self.assertEqual(equipment.spoonacular_id, 456)
        self.assertEqual(equipment.picture, "http://example.com/oven.jpg")