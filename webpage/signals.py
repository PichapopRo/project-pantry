from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Recipe, Profile

@receiver(post_save, sender=Recipe)
def check_approved_recipes(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        user = instance.poster_id
        approved_recipes_count = Recipe.objects.filter(poster_id=user, status='approved').count()
        if approved_recipes_count >= 10:
            profile, created = Profile.objects.get_or_create(user=user)  # Get or create the user's profile
            profile.chef_badge = True
            profile.save()