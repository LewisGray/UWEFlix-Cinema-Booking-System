# Generated by Django 4.0.2 on 2022-04-07 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0004_notification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link_data',
            field=models.CharField(default='', max_length=500),
        ),
    ]
