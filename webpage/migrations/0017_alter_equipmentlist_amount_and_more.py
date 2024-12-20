# Generated by Django 5.1.1 on 2024-10-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0016_alter_equipment_picture_alter_ingredient_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentlist',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingredientlist',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
