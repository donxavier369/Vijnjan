# Generated by Django 4.2.11 on 2024-05-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_remove_files_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modules',
            name='module_content_ppt',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='modules',
            name='module_content_video',
            field=models.CharField(blank=True, null=True),
        ),
    ]
