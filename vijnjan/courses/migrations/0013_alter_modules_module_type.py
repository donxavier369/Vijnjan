# Generated by Django 4.2.11 on 2024-05-04 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modules',
            name='module_type',
            field=models.CharField(choices=[('video', 'Video'), ('ppt', 'ppt')], default='ppt'),
        ),
    ]
