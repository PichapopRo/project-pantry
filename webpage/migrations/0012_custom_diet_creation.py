from django.db import migrations

def create_default_diets(apps, schema_editor):
    Diet = apps.get_model('webpage', 'Diet')
    Diet.objects.bulk_create([
        Diet(name="vegan"),
        Diet(name="vegetarian"),
        Diet(name="pescatarian"),
        Diet(name="gluten-free"),
        Diet(name="paleo"),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_diet_recipe_diets'),
    ]

    operations = [
        migrations.RunPython(create_default_diets),
    ]