"""URL configuration for the recipe application."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("<int:pk>/", views.RecipeView.as_view(), name="recipe"),
    path("randomizer/", views.random_recipe_view, name="random_recipe"),
    path('<int:recipe_id>/toggle_favourite/', views.toggle_favourite, name='toggle_favorite'),
    path('add_recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('<int:pk>/edit/', views.EditRecipeView.as_view(), name='edit_recipe'),
]
