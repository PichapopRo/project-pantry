import json
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import User
from django import forms
from .models import Recipe


class CustomRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
        help_texts = {
            'username': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        return cleaned_data


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'estimated_time', 'diets', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    ingredients_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    equipment_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    steps_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_ingredients_data(self):
        """Validate and parse ingredients data as JSON."""
        ingredients = self.cleaned_data.get('ingredients_data', '[]')
        try:
            ingredients = json.loads(ingredients)
            if not isinstance(ingredients, list):
                raise ValidationError("Invalid format for ingredients data.")
        except json.JSONDecodeError:
            raise ValidationError("Ingredients data must be valid JSON.")
        return ingredients

    def clean_equipment_data(self):
        """Validate and parse equipment data as JSON."""
        equipment = self.cleaned_data.get('equipment_data', '[]')
        try:
            equipment = json.loads(equipment)
            if not isinstance(equipment, list):
                raise ValidationError("Invalid format for equipment data.")
        except json.JSONDecodeError:
            raise ValidationError("Equipment data must be valid JSON.")
        return equipment

    def clean_steps_data(self):
        """Validate and parse steps data as JSON."""
        steps = self.cleaned_data.get('steps_data', '[]')
        try:
            steps = json.loads(steps)
            if not isinstance(steps, list):
                raise ValidationError("Invalid format for steps data.")
        except json.JSONDecodeError:
            raise ValidationError("Steps data must be valid JSON.")
        return steps
