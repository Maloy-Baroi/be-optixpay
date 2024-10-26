# Generated by Django 5.1.2 on 2024-10-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payment', '0006_alter_historicalpayment_paymentid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_from', models.CharField(max_length=50)),
                ('converted_to', models.CharField(max_length=50)),
                ('amount_per_unit', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]