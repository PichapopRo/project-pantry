# Generated by Django 5.1.1 on 2024-10-18 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0008_alter_recipe_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='images',
            new_name='image',
        ),
    ]
