# Generated by Django 5.0.3 on 2024-03-25 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_modules_module_content_ppt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_trending',
            field=models.BooleanField(default=False),
        ),
    ]
