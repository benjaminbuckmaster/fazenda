# Generated by Django 5.0.2 on 2024-02-16 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_stockoffset_total_stock_quantity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockentry',
            unique_together={('bean', 'date')},
        ),
    ]