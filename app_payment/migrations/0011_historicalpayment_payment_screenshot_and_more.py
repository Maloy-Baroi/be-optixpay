# Generated by Django 4.2.16 on 2024-10-28 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payment', '0010_historicalpayment_in_bdt_payment_in_bdt'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpayment',
            name='payment_screenshot',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='payment/screenshots'),
        ),
    ]
