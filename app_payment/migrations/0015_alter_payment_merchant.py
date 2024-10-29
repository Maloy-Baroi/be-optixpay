# Generated by Django 4.2.16 on 2024-10-28 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_merchant', '0006_alter_historicalmerchant_is_active_and_more'),
        ('app_payment', '0014_cryptoaddresstrc_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_merchant', to='app_merchant.merchant'),
        ),
    ]
