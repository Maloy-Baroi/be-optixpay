# Generated by Django 4.2.16 on 2024-10-29 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_agent', '0009_paymentprovider_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentprovider',
            name='maximum_transaction_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentprovider',
            name='minimum_transaction_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]
