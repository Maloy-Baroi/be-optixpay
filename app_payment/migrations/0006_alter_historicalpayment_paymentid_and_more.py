# Generated by Django 5.1.2 on 2024-10-20 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payment', '0005_alter_historicalpayment_trxid_alter_payment_trxid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpayment',
            name='paymentID',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentID',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
