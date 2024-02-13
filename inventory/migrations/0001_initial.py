# Generated by Django 5.0.2 on 2024-02-12 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('origin', models.CharField(max_length=50)),
                ('supplier', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=500)),
                ('reorder_trigger', models.DecimalField(decimal_places=2, max_digits=5)),
                ('reorder_qty', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]