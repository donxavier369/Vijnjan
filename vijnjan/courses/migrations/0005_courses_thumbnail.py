# Generated by Django 5.0.3 on 2024-04-01 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_courses_is_trending'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='thumbnail',
            field=models.ImageField(default=0, upload_to='courses/thumbnail'),
            preserve_default=False,
        ),
    ]