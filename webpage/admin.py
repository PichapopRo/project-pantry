from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Recipe, IngredientList, EquipmentList, NutritionList


class IngredientListInline(admin.TabularInline):
    model = IngredientList
    extra = 1
    readonly_fields = ['ingredient', 'amount', 'unit']
    verbose_name = "Ingredient"
    verbose_name_plural = "Ingredients"

class EquipmentListInline(admin.TabularInline):
    model = EquipmentList
    extra = 1
    readonly_fields = ['equipment', 'amount', 'unit']
    verbose_name = "Equipment"
    verbose_name_plural = "Equipment List"

class NutritionListInline(admin.TabularInline):
    model = NutritionList
    extra = 1
    readonly_fields = ['nutrition', 'amount', 'unit']
    verbose_name = "Nutrition"
    verbose_name_plural = "Nutrition List"

class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 100}),
        }

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ('name', 'poster_id', 'created_at', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('name', 'description')
    inlines = [IngredientListInline, EquipmentListInline, NutritionListInline]

admin.register(User)
admin.site.register(Recipe, RecipeAdmin)
