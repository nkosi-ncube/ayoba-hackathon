# Generated by Django 5.0.7 on 2024-07-24 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gatewayapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='permissions',
            field=models.JSONField(default=dict),
        ),
    ]
