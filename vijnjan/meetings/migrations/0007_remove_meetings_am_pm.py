# Generated by Django 4.2.11 on 2024-05-06 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_meetings_am_pm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetings',
            name='am_pm',
        ),
    ]
