from django.db import migrations

def create_default_diets(apps, schema_editor):
    Diet = apps.get_model('webpage', 'Diet')
    Diet.objects.bulk_create([
        Diet(name="Vegan"),
        Diet(name="Vegetarian"),
        Diet(name="Pescatarian"),
        Diet(name="Gluten free"),
        Diet(name="Paleo"),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_diet_recipe_diets'),
    ]

    operations = [
        migrations.RunPython(create_default_diets),
    ]