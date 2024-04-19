# Generated by Django 3.2.15 on 2022-11-24 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0006_delete_door_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Door_event',
            fields=[
                ('time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('state', models.SmallIntegerField()),
                ('bei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='door_event_bei', to='dashboard.bei')),
            ],
        ),
    ]
