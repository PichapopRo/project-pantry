# Generated by Django 5.1.2 on 2024-10-19 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_nutrition_nutritionlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrition',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
