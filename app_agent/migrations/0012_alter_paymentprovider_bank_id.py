# Generated by Django 4.2.16 on 2024-10-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_agent', '0011_paymentprovider_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentprovider',
            name='bank_id',
            field=models.CharField(default='ag-d9cef9c4-803f-4e74-8c39-214733c70629', max_length=200),
        ),
    ]
