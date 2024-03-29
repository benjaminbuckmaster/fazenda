# Generated by Django 5.0.2 on 2024-02-15 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_bean_notes_alter_bean_origin_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockentry',
            options={'verbose_name': 'Stock Entry', 'verbose_name_plural': 'Stock Entries'},
        ),
        migrations.RemoveField(
            model_name='stockentry',
            name='qty_total',
        ),
        migrations.CreateModel(
            name='ManualStockOffset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_offset', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total_stock_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('bean', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manual_stock_offset', to='inventory.bean')),
            ],
        ),
    ]
