from django.db import migrations

def create_default_cuisine(apps, schema_editor):
    Cuisine = apps.get_model('webpage', 'Cuisine')
    Cuisine.objects.bulk_create([
        Cuisine(name="Japanese"),
        Cuisine(name="Korean"),
        Cuisine(name="Irish"),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0025_alter_recipe_image'),
    ]

    operations = [
        migrations.RunPython(create_default_cuisine),
    ]