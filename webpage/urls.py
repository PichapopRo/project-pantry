"""URL configuration for the recipe application."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("<int:pk>/", views.RecipeView.as_view(), name="recipe"),
    path("<int:pk>/steps/", views.StepView.as_view(), name="steps"),
    path("randomizer/", views.RandomizerView.as_view(), name="randomizer"),
]
