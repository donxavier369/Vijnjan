# Generated by Django 5.0.3 on 2024-04-08 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_meetings_delete_meatings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetings',
            name='meeting_name',
        ),
        migrations.AddField(
            model_name='meetings',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='meetings',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='meetings',
            name='time',
            field=models.TimeField(),
        ),
    ]
