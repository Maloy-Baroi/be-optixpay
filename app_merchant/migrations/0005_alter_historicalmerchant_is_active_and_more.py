# Generated by Django 5.1.1 on 2024-10-01 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_merchant', '0004_alter_historicalmerchant_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmerchant',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
