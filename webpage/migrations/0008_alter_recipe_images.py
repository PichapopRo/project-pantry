# Generated by Django 5.1.1 on 2024-10-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0007_alter_recipe_poster_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='images',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
