# Generated by Django 5.0.4 on 2024-06-04 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_remove_grid_minute_remove_grid_time_grid_name_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='grid',
            table='Grid',
        ),
        migrations.AlterModelTable(
            name='task',
            table='Task',
        ),
    ]
