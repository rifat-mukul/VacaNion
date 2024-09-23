# Generated by Django 5.0.6 on 2024-09-23 03:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_reviewrating_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattable',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='rating',
            field=models.FloatField(default=10),
        ),
    ]