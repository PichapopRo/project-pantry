from .models import Recipe

def award_chef_badge(user):
    approved_recipe_count = Recipe.objects.filter(poster_id=user, status='approved').count()

    if approved_recipe_count >= 10:
        user.profile.chef_badge = True
        user.profile.save()