# Generated by Django 5.1.1 on 2024-10-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0010_alter_agentprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentprofile',
            name='is_active',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('hold', 'Hold'), ('soft_deleted', 'Soft Deleted')], default='inactive', max_length=20),
        ),
    ]
