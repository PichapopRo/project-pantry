from django.db import migrations

def create_default_diets(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_diet_recipe_diets'),
    ]

    operations = [
        migrations.RunPython(create_default_diets),
    ]