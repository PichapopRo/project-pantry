"""This module contains functionality related to awarding badges to users."""
from webpage.models import Recipe
from decouple import config


def award_chef_badge(user):
    """
    Awards a chef badge to a user who has at least 10 approved recipes.

    :param user: The user to check for approved recipes and award the chef badge.
                 The user must have a related `Profile` model where the `chef_badge` field is stored.
    """
    chef_badge_approved_amount = config('CHEF_BADGE_APPROVED', cast=int, default=10)
    approved_recipe_count = Recipe.objects.filter(poster_id=user, status='approved').count()

    if approved_recipe_count >= chef_badge_approved_amount:
        user.profile.chef_badge = True
        user.profile.save()
