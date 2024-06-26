# Generated by Django 4.2.11 on 2024-05-20 17:20

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_gender_alter_customuser_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile/profile_image', validators=[accounts.models.validate_profile_image_size]),
        ),
    ]
