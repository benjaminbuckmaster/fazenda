# Generated by Django 5.0.1 on 2024-06-18 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_blendcomponent_delete_blendbean'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blendcomponent',
            name='blend',
        ),
        migrations.RemoveField(
            model_name='blendcomponent',
            name='bean',
        ),
        migrations.DeleteModel(
            name='Blend',
        ),
        migrations.DeleteModel(
            name='BlendComponent',
        ),
    ]
