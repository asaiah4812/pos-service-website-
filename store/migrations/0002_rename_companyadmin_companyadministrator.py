# Generated by Django 5.0.7 on 2024-07-22 21:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompanyAdmin',
            new_name='CompanyAdministrator',
        ),
    ]
