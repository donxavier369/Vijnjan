# Generated by Django 4.2.11 on 2024-05-06 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_alter_meetings_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetings',
            name='am_pm',
            field=models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], default='AM', max_length=2),
        ),
    ]
