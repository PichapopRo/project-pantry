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
        """Validate and parse ingredients data."""
        ingredients = self.cleaned_data.get('ingredients_data')
        # Validate or parse ingredients JSON if needed
        return ingredients

    def clean_equipment_data(self):
        """Validate and parse equipment data."""
        equipment = self.cleaned_data.get('equipment_data')
        # Validate or parse equipment JSON if needed
        return equipment

    def clean_steps_data(self):
        """Validate and parse steps data."""
        steps = self.cleaned_data.get('steps_data')
        # Validate or parse steps JSON if needed
        return steps

    def save(self, commit=True):
        recipe = super().save(commit=False)
        # Handle parsed JSON data here, if additional processing is needed
        if commit:
            recipe.save()
        return recipe
