from django.views import generic
from .models import *


class RecipeListView(generic.ListView):
    """RecipeList view."""

    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        """Return recipes limited by view_count."""
        if 'view_count' not in self.request.session:
            self.request.session['view_count'] = 5
        all_recipes = Recipe.objects.all()
        view_count = self.request.session['view_count']
        return all_recipes[:view_count]

    def post(self, request, *args, **kwargs):
        """Handle POST request to increment view_count."""
        if 'increment' in self.request.POST:
            increment = int(self.request.POST.get('increment', 0))
            self.request.session['view_count'] += increment
        elif 'reset' in self.request.POST:
            self.request.session['view_count'] = 5
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the current view_count to the context."""
        context = super().get_context_data(**kwargs)
        context['view_count'] = self.request.session['view_count']
        return context


class RecipeView(generic.DetailView):
    """RecipeView view."""
    template_name = 'recipes/recipe.html'
    model = Recipe
    context_object_name = 'recipe'
