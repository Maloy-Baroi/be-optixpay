# Generated by Django 5.1.1 on 2024-10-01 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='historicalcurrency',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
