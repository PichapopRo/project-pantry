from django.views import generic
from .models import *


class RecipeListView(generic.ListView):
    """RecipeList view."""

    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        """Return recipes limited by view_count."""
        view_count = self.request.session.get('view_count', 0)
        all_recipes = Recipe.objects.all()
        return all_recipes[:view_count]

    def post(self, request, *args, **kwargs):
        """Handle POST request to increment view_count."""
        if 'increment' in request.POST:
            increment = int(request.POST.get('increment', 0))
            request.session['view_count'] = request.session.get('view_count', 0) + increment
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add the current view_count to the context."""
        context = super().get_context_data(**kwargs)
        context['total_recipes'] = Recipe.objects.count()
        context['view_count'] = self.request.session.get('view_count', 0)
        return context


class RecipeView(generic.DetailView):
    """RecipeView view."""
    template_name = 'recipes/recipe.html'
    model = Recipe
    context_object_name = 'recipe'
