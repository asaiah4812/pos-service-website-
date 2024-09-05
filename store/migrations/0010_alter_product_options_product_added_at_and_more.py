# Generated by Django 5.0.7 on 2024-07-26 12:39

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_buyer_company_supplier_company'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-added_at',)},
        ),
        migrations.AddField(
            model_name='product',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.company'),
        ),
        migrations.AddField(
            model_name='product',
            name='expdate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='product',
            name='mfdate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='store.supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouses', to='store.company'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='store.company'),
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Dreamer_Warehouses',
                'ordering': ('-created_at',),
            },
        ),
    ]