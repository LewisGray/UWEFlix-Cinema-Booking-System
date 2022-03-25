# Generated by Django 4.0.2 on 2022-03-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0004_showing_taken_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='adult_tickets',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='child_tickets',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='student_tickets',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]