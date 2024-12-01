"""Tests for the FilterParam class."""

from django.test import TestCase
from webpage.modules.filter_objects import FilterParam


class FilterParamTest(TestCase):
    """Test the FilterParam model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data and mocks."""
        cls.default_filter = FilterParam(
            offset=0,
            number=10)
        cls.custom_filter = FilterParam(
            offset=1,
            number=5,
            includeIngredients=["tomato", "apple"],
            diet=["vegetarian", "vegan"],
            maxReadyTime=30,
            titleMatch="salad"
        )

    def test_default_create(self):
        """Test if the FilterParam object is created correctly for default FilterParam."""
        self.assertIsInstance(self.default_filter, FilterParam)
        self.assertEqual(self.default_filter.offset, 0)
        self.assertEqual(self.default_filter.number, 10)
        self.assertEqual(self.default_filter.includeIngredients, [])
        self.assertEqual(self.default_filter.diet, [])
        self.assertEqual(self.default_filter.maxReadyTime, 9999)
        self.assertEqual(self.default_filter.titleMatch, "")

    def test_custom_create(self):
        """Test if the FilterParam object is created correctly for custom FilterParam."""
        self.assertIsInstance(self.custom_filter, FilterParam)
        self.assertEqual(self.custom_filter.offset, 1)
        self.assertEqual(self.custom_filter.number, 5)
        self.assertEqual(self.custom_filter.includeIngredients,
                         ["tomato", "apple"])
        self.assertEqual(self.custom_filter.diet,
                         ["vegetarian", "vegan"])
        self.assertEqual(self.custom_filter.maxReadyTime, 30)
        self.assertEqual(self.custom_filter.titleMatch, "salad")

    def test_default_add_ingredient(self):
        """Test the add_ingredient for default FilterParam."""
        self.default_filter.add_ingredient("cheese")
        self.assertEqual(len(self.default_filter.includeIngredients), 1)
        self.assertEqual(self.default_filter.includeIngredients,
                         ["cheese"])

    def test_custom_add_ingredient(self):
        """Test the add_ingredient for custom FilterParam."""
        self.custom_filter.add_ingredient("cheese")
        self.assertEqual(len(self.custom_filter.includeIngredients), 3)
        self.assertEqual(self.custom_filter.includeIngredients,
                         ["tomato", "apple", "cheese"])

    def test_default_get_param(self):
        """Test the get_param for default FilterParam."""
        expected_get_param_default = {
            'includeIngredients': [],
            'diet': [],
            'maxReadyTime': 9999,
            'titleMatch': "",
            'cuisine': ''
        }
        self.assertEqual(self.default_filter.get_param(),
                         expected_get_param_default)

    def test_custom_get_param(self):
        """Test the get_param for custom FilterParam."""
        expected_get_param_custom = {
            'includeIngredients': ["tomato", "apple"],
            'diet': ["vegetarian", "vegan"],
            'maxReadyTime': 30,
            'titleMatch': "salad",
            'cuisine': ''
        }
        self.assertEqual(self.custom_filter.get_param(),
                         expected_get_param_custom)

    def test_default_repr(self):
        """Test the repr representation of the default FilterParam."""
        expected_repr_default = ("FilterParam("
                                 "offset=0, "
                                 "number=10, "
                                 "includeIngredients=[], "
                                 "diet=[], "
                                 "maxReadyTime=9999, "
                                 "titleMatch=)")
        self.assertEqual(repr(self.default_filter), expected_repr_default)

    def test_custom_repr(self):
        """Test the repr representation of the custom FilterParam."""
        expected_repr_custom = ("FilterParam("
                                "offset=1, "
                                "number=5, "
                                "includeIngredients=['tomato', 'apple'], "
                                "diet=['vegetarian', 'vegan'], "
                                "maxReadyTime=30, "
                                "titleMatch=salad)")
        self.assertEqual(repr(self.custom_filter), expected_repr_custom)
