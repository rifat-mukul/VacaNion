# Generated by Django 5.0.6 on 2024-09-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_reviewratings_reviewrating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profileimg',
            field=models.ImageField(blank=True, default='blank-profile-picture.png', upload_to='profileimg'),
        ),
    ]
