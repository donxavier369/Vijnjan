# Generated by Django 4.2.11 on 2024-05-13 07:55

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_alter_modules_module_content_ppt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='thumbnail',
            field=models.ImageField(default=0, upload_to='courses/thumbnail', validators=[courses.models.validate_thumbnail_size]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courses',
            name='thumbnail',
            field=models.CharField(default='thumbnail'),
        ),
    ]