# Generated by Django 4.2.16 on 2024-10-28 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payment', '0013_historicalpayment_address_trc_payment_address_trc'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptoaddresstrc',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]