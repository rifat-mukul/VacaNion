# Generated by Django 5.0.6 on 2024-09-13 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_reviewrating_hotel_alter_reviewrating_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='user',
        ),
    ]
