# Generated by Django 5.0.1 on 2024-05-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_productbean_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bean',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productbean',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=10),
        ),
    ]
