import json
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import User


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


from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'estimated_time', 'diets', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    # Additional fields for ingredients, equipment, and steps
    ingredients_data = forms.CharField(widget=forms.HiddenInput())
    equipment_data = forms.CharField(widget=forms.HiddenInput())
    steps_data = forms.CharField(widget=forms.HiddenInput())

    def clean_ingredients_data(self):
        """Validate and parse ingredients data as JSON."""
        ingredients = self.cleaned_data.get('ingredients_data')
        try:
            ingredients = json.loads(ingredients)  # Parse JSON
            if not isinstance(ingredients, list):
                raise ValidationError("Invalid format for ingredients data.")
        except (json.JSONDecodeError, ValidationError):
            raise ValidationError("Ingredients data must be a valid JSON list.")
        return ingredients

    def clean_equipment_data(self):
        """Validate and parse equipment data as JSON."""
        equipment = self.cleaned_data.get('equipment_data')
        try:
            equipment = json.loads(equipment)  # Parse JSON
            if not isinstance(equipment, list):
                raise ValidationError("Invalid format for equipment data.")
        except (json.JSONDecodeError, ValidationError):
            raise ValidationError("Equipment data must be a valid JSON list.")
        return equipment

    def clean_steps_data(self):
        """Validate and parse steps data as JSON."""
        steps = self.cleaned_data.get('steps_data')
        try:
            steps = json.loads(steps)  # Parse JSON
            if not isinstance(steps, list):
                raise ValidationError("Invalid format for steps data.")
        except (json.JSONDecodeError, ValidationError):
            raise ValidationError("Steps data must be a valid JSON list.")
        return steps

    def save(self, commit=True):
        recipe = super().save(commit=False)

        # Store parsed data for use in the view if necessary
        self.instance.ingredients_data = self.cleaned_data['ingredients_data']
        self.instance.equipment_data = self.cleaned_data['equipment_data']
        self.instance.steps_data = self.cleaned_data['steps_data']

        if commit:
            recipe.save()
        return recipe
