# Generated by Django 4.0.3 on 2022-03-28 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0005_booking_adult_tickets_booking_child_tickets_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Screen',
            new_name='Screens',
        ),
        migrations.DeleteModel(
            name='Cinema',
        ),
    ]
