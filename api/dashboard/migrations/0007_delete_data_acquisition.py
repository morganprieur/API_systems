# Generated by Django 3.2.15 on 2022-11-24 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_delete_door_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Data_acquisition',
        ),
    ]