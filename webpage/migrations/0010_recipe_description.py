# Generated by Django 5.1.2 on 2024-10-18 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0009_rename_images_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
