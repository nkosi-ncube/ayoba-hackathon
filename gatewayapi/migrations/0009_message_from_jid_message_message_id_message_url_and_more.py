# Generated by Django 5.0.7 on 2024-07-26 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gatewayapi', '0008_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='from_jid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='message_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='msisdn',
            field=models.CharField(max_length=15),
        ),
    ]
