# Generated by Django 5.0.7 on 2024-07-25 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_developer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_buyer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_supplier',
            field=models.BooleanField(default=False),
        ),
    ]
