# Generated by Django 5.0.1 on 2024-05-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_bean_is_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bean',
            name='is_hidden',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='bean',
            name='is_ordered',
            field=models.BooleanField(),
        ),
    ]
