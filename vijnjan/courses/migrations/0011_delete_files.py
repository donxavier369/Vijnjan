# Generated by Django 4.2.11 on 2024-04-24 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_files'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Files',
        ),
    ]