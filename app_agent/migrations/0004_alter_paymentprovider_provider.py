# Generated by Django 5.1.2 on 2024-10-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_agent', '0003_alter_paymentprovider_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentprovider',
            name='provider',
            field=models.CharField(choices=[('bkash', 'bKash'), ('nagad', 'Nagad'), ('stripe', 'Stripe'), ('paypal', 'PayPal')], default='bkash', max_length=50),
        ),
    ]
